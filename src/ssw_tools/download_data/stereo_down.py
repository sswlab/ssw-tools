"""
STEREO data download module
@author: Junmu Youn (jmyoun@khu.ac.kr)  
"""


from sunpy.net import Fido, attrs as a
import os
from datetime import datetime, timedelta
import astropy.units as u
from dateutil.relativedelta import relativedelta
import argparse
import pandas as pd


def minute_range_list(center_time_str):
    # center_time_str: "YYYYMMDDHHMM"
    center = datetime.strptime(center_time_str, "%Y%m%d%H%M")
    minute_list = []
    for delta in range(-10, 11):  # -10 ~ +10분 (총 21개)
        t = center + timedelta(minutes=delta)
        minute_list.append(t.strftime("%Y%m%d%H%M"))
    return minute_list

#STEREO
def run_stereo(start_date: datetime, end_date: datetime, delta_hours: int, out_path: str,
             level: int = 1, tolerance_min: int = 15, cadence_min: int = 60):
    
    out_path171 = os.path.join(out_path, 'stereo-174')
    out_path304 =  os.path.join(out_path, 'stereo-304') 
    os.makedirs(out_path171, exist_ok=True)
    os.makedirs(out_path304, exist_ok=True)   

    if end_date is None:
        end_date = start_date

    while start_date <= end_date:

        start_delta = start_date - relativedelta(hours=delta_hours)
        end_delta = start_date + relativedelta(hours=delta_hours)
        qr = Fido.search(
            a.Time(start_delta, end_delta), 
            a.Provider('SSC'),
            a.Instrument('EUVI'), #EUVI
            a.Source('STEREO_A'), #STEREO_A
            a.Wavelength(171*u.AA) | a.Wavelength(304*u.AA),
        )
        tbl_171 = qr[0]
        names_1d_171 = [name for name in tbl_171.colnames if name != 'Wavelength']
        df_171 = tbl_171[names_1d_171].to_pandas()
        df_171['Wavelength'] = 171 # 파장 값을 직접 추가

        tbl_304 = qr[1]
        names_1d_304 = [name for name in tbl_304.colnames if name != 'Wavelength']
        df_304 = tbl_304[names_1d_304].to_pandas()
        df_304['Wavelength'] = 304 # 파장 값을 직접 추가

        # reset_index 대신, 인덱스를 새 열에 직접 복사합니다. 이 방법이 더 안정적입니다.
        df_171['original_index_171'] = df_171.index
        df_304['original_index_304'] = df_304.index

        # 시간 변환 및 정렬
        df_171['Start Time'] = pd.to_datetime(df_171['Start Time'])
        df_304['Start Time'] = pd.to_datetime(df_304['Start Time'])
        df_171.sort_values('Start Time', inplace=True)
        df_304.sort_values('Start Time', inplace=True)

        # 열 이름 변경
        df_171.rename(columns={'Start Time': 'Start Time_171'}, inplace=True)
        df_304.rename(columns={'Start Time': 'Start Time_304'}, inplace=True)

        # left_on과 right_on을 사용하여 병합
        paired_df = pd.merge_asof(
            df_171,
            df_304,
            left_on='Start Time_171',
            right_on='Start Time_304',
            tolerance=pd.Timedelta(minutes=15),
            direction='nearest',
            suffixes=('_171', '_304')
        )

        paired_df.dropna(subset=['Source_304'], inplace=True)

        # print("\n------------ 15분 이내로 촬영된 데이터 쌍 후보 ------------")
        # print(paired_df[['Start Time_171', 'Start Time_304']])

        # 3. 기준 시간과 가장 가까운 쌍 선택 및 다운로드
        # ----------------------------------------------------------------
        if not paired_df.empty:
            # 각 쌍의 171 Å 촬영 시간과 start_date 사이의 시간 차이 계산
            paired_df['time_diff_from_start'] = (paired_df['Start Time_171'] - start_date).abs()

            # 시간 차이가 가장 작은 쌍을 선택
            closest_pair = paired_df.loc[paired_df['time_diff_from_start'].idxmin()]

            print(f"\n------------ Nearest from {start_date} ------------")
            print(closest_pair[['Start Time_171', 'Start Time_304']])

            # 다운로드할 데이터의 원본 인덱스 추출
            index_171 = int(closest_pair['original_index_171'])
            index_304 = int(closest_pair['original_index_304'])

            # 원본 검색 결과(qr)에서 다운로드할 데이터 선택
            file_171 = qr[0][index_171]
            file_304 = qr[1][index_304]

            print("\n------------ Download ------------")

            # download both selected files
            downloaded_file171 = Fido.fetch(file_171, path=out_path171)
            downloaded_file304 = Fido.fetch(file_304, path=out_path304)
    

            print("\n------------ Download Complete ------------")
            print(downloaded_file171)
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
    # main.py에서 args를 넘겨주는 경우 그대로 사용
    if args is not None and hasattr(args, "start_date"):
        sd = datetime.strptime(args.start_date, "%Y-%m-%dT%H:%M")
        ed = datetime.strptime(args.end_date, "%Y-%m-%dT%H:%M") if args.end_date else None
        run_stereo(sd, ed, args.delta_hours, args.out_path, args.level, args.tolerance_min, args.cadence_min)
        return

    # 단독 실행 지원
    import argparse
    p = add_args(argparse.ArgumentParser())
    a = p.parse_args()
    sd = datetime.strptime(a.start_date, "%Y-%m-%dT%H:%M")
    ed = datetime.strptime(a.end_date, "%Y-%m-%dT%H:%M") if a.end_date else None
    run_stereo(sd, ed, a.delta_hours, a.out_path, a.level, a.tolerance_min, a.cadence_min)

if __name__ == "__main__":
    main()