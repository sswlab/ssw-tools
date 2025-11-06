"""
Solar Orbiter data download module
@author: Junmu Youn (jmyoun@khu.ac.kr)  
"""

from sunpy.net import Fido, attrs as a
import os
from datetime import datetime, timedelta
import sunpy_soar
from dateutil.relativedelta import relativedelta
import pandas as pd

def minute_range_list(center_time_str):
    # center_time_str: "YYYYMMDDHHMM"
    center = datetime.strptime(center_time_str, "%Y%m%d%H%M")
    minute_list = []
    for delta in range(-10, 11):  # -10 ~ +10분 (총 21개)
        t = center + timedelta(minutes=delta)
        minute_list.append(t.strftime("%Y%m%d%H%M"))
    return minute_list


#SolO
def run_solo(start_date: datetime, end_date: datetime, delta_hours: int, out_path: str,
             level: int = 1, tolerance_min: int = 15, cadence_min: int = 60):
    
    out_path174 = os.path.join(out_path, 'solo/174')
    out_path304 =  os.path.join(out_path, 'solo/304') 
    os.makedirs(out_path174, exist_ok=True)
    os.makedirs(out_path304, exist_ok=True)   


    if end_date is None:
        end_date = start_date

    while start_date <= end_date:

        start_delta = start_date - relativedelta(hours=delta_hours)
        end_delta   = start_date + relativedelta(hours=delta_hours)
        os.makedirs(out_path, exist_ok=True)    
        qr_174 = Fido.search(
            a.Time(start_delta, end_delta),
            a.Instrument('EUI'),
            a.Level(level),
            a.soar.Product('eui-fsi174-image'),
        )

        qr_304 = Fido.search(
            a.Time(start_delta, end_delta),
            a.Instrument('EUI'),
            a.Level(level),
            a.soar.Product('eui-fsi304-image'),
        )


        # ----------------------------------------------------------------
        # 데이터 처리 및 다운로드
        # ----------------------------------------------------------------
        df_174 = qr_174[0].to_pandas() if qr_174 and len(qr_174[0]) > 0 else pd.DataFrame()
        df_304 = qr_304[0].to_pandas() if qr_304 and len(qr_304[0]) > 0 else pd.DataFrame()

        if df_174.empty or df_304.empty:
            print("\n두 파장의 데이터가 모두 존재하지 않아 쌍을 찾을 수 없습니다.")
        else:
            # 인덱스를 새 열에 직접 복사
            df_174['original_index_174'] = df_174.index
            df_304['original_index_304'] = df_304.index


            # 시간 변환 및 정렬 'Start Time' -> 'Start time' (소문자 t)
            df_174['Start time'] = pd.to_datetime(df_174['Start time'])
            df_304['Start time'] = pd.to_datetime(df_304['Start time'])
            df_174.sort_values('Start time', inplace=True)
            df_304.sort_values('Start time', inplace=True)

            # 열 이름 변경
            df_174.rename(columns={'Start time': 'Start Time_174'}, inplace=True)
            df_304.rename(columns={'Start time': 'Start Time_304'}, inplace=True)

            # left_on과 right_on을 사용하여 병합
            paired_df = pd.merge_asof(
                df_174,
                df_304,
                left_on='Start Time_174',
                right_on='Start Time_304',
                tolerance=pd.Timedelta(minutes=tolerance_min),
                direction='nearest',
                suffixes=('_174', '_304')
            )

            paired_df.dropna(subset=['Start Time_304'], inplace=True)

            if not paired_df.empty:
                print("\n------------ 15분 이내로 촬영된 데이터 쌍 후보 ------------")
                print(paired_df[['Start Time_174', 'Start Time_304']])

                # 기준 시간과 가장 가까운 쌍 선택
                paired_df['time_diff_from_start'] = (paired_df['Start Time_174'] - start_date).abs()
                closest_pair = paired_df.loc[paired_df['time_diff_from_start'].idxmin()]

                print(f"\n------------ Nearest from {start_date} ------------")
                print(closest_pair[['Start Time_174', 'Start Time_304']])

                # 다운로드할 데이터의 원본 인덱스 추출
                index_174 = int(closest_pair['original_index_174'])
                index_304 = int(closest_pair['original_index_304'])

                # 원본 검색 결과에서 다운로드할 데이터 선택
                file_174 = qr_174[0][index_174]
                file_304 = qr_304[0][index_304]

                # print("\n------------ 다운로드 대상 ------------")

                # download both selected files
                downloaded_file174 = Fido.fetch(file_174, path=out_path174)
                downloaded_file304 = Fido.fetch(file_304, path=out_path304)
        

                print("\n------------ Download Complete ------------")
                print(downloaded_file174)
                print(downloaded_file304)

            else:
                print("No data")

        start_date += relativedelta(minutes=cadence_min)
            
def add_args(parser):
    parser.add_argument("--start_date", required=True, help="YYYY-mm-ddTHH:MM")
    parser.add_argument("--end_date", help="YYYY-mm-ddTHH:MM", default=None)
    parser.add_argument("--delta_hours", type=int, default=12)
    parser.add_argument("--out_path", default="/userhome/youn_j/project/IITP/dataset/")
    parser.add_argument("--level", type=int, choices=[1, 2], default=1, help="SOAR processing level")
    parser.add_argument("--tolerance_min", type=int, default=15, help="pairing tolerance in minutes")
    parser.add_argument("--cadence_min", type=int, default=60*24, help="minimum cadence in minutes")
    return parser

def main(args=None):
    if args is not None and hasattr(args, "start_date"):
        sd = datetime.strptime(args.start_date, "%Y-%m-%dT%H:%M")
        run_solo(sd, ed, args.delta_hours, args.out_path, args.level, args.tolerance_min, args.cadence_min)
        return

    import argparse
    p = add_args(argparse.ArgumentParser())
    a = p.parse_args()
    sd = datetime.strptime(a.start_date, "%Y-%m-%dT%H:%M")
    ed = datetime.strptime(a.end_date, "%Y-%m-%dT%H:%M") if a.end_date else None
    run_solo(sd, ed, a.delta_hours, a.out_path, a.level, a.tolerance_min, a.cadence_min)

if __name__ == "__main__":
    main()