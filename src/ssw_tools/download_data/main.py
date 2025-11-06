"""
@author: Junmu Youn (jmyoun@khu.ac.kr)  
"""

# main.py
# e.g.) python main.py --target stereo --start_date 2012-07-15T00:00

import argparse
import datetime
from stereo_down import main as stereo_main
from solo_down import main as solo_main

TABLE = {
    "stereo-a": stereo_main,
    "stereo-b": stereo_main,
    "solo": solo_main,
}

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--target", choices=TABLE.keys(), required=True)
    p.add_argument("--start_date", required=True, help="YYYY-mm-ddTHH:MM")
    p.add_argument("--end_date", help="YYYY-mm-ddTHH:MM", default=None)
    p.add_argument("--delta_hours", type=int, default=12)
    p.add_argument("--out_path", default="/userhome/youn_j/project/IITP/dataset/")
    p.add_argument("--level", type=int, choices=[1, 2], default=1)
    p.add_argument("--tolerance_min", type=int, default=15)
    p.add_argument("--cadence_min", type=int, default=60*24)
    return p.parse_args()

def main():
    args = parse_args()
    # start date가 현재 시각 1주일 이내인 경우 solo_nrt.py를 사용하도록 강제 (tbd)
    # if datetime(args.start_date) > datetime.now() - datetime.timedelta(weeks=1):
    #     args.target = "solo_nrt"

    TABLE[args.target](args)

if __name__ == "__main__":
    main()