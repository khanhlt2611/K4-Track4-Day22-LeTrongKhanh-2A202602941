"""Chạy cấu hình cuối trên toàn bộ ảnh và giữ nhật ký từng video."""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main() -> None:
    """Đọc cấu hình cuối và tạo năm file kết quả đủ frame."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab-data-root',type=Path,default=Path('data_lab21'))
    parser.add_argument('--config',type=Path,default=Path('submission_template/cau_hinh.json'))
    parser.add_argument('--out',type=Path,default=Path('runs/nop_bai'))
    parser.add_argument('--device',default='cuda:0')
    parser.add_argument('--videos',nargs='+',default=[f'video_{i}' for i in range(1,6)])
    parser.add_argument('--workers',type=int,default=1)
    args=parser.parse_args()
    configs=json.loads(args.config.read_text(encoding='utf-8-sig'))
    args.out.mkdir(parents=True,exist_ok=True)

    def run_one(video: str) -> None:
        """Chạy toàn bộ một video và kiểm tra mã thoát.

        Args:
            video: Tên video trong cấu hình cuối.
        """
        config=configs[video]
        metadata_path=args.out/f'{video}_run.json'
        if metadata_path.exists():
            record=json.loads(metadata_path.read_text(encoding='utf-8'))
            expected=len(list((args.lab_data_root/video/'img1').glob('*.jpg')))
            if all(record[key]==config[key] for key in ('tracker','conf','iou')) and record['max_frames']==0 and record['frames']==expected and (args.out/f'{video}.txt').exists():
                print(f'{video}: đã có kết quả đủ frame đúng cấu hình',flush=True)
                return
        command=[sys.executable,'-u','scripts/run_tracking.py','--source',str(args.lab_data_root/video/'img1'),
                 '--seq-name',video,'--tracker',config['tracker'],'--conf',str(config['conf']),
                 '--iou',str(config['iou']),'--out',str(args.out),'--save-video','--device',args.device]
        print(f'Đang chạy bản nộp {video}',flush=True)
        with (args.out/f'{video}_log.txt').open('w',encoding='utf-8') as log:
            subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
        print(f'Đã chạy đủ frame {video}',flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        list(executor.map(run_one,args.videos))


if __name__=='__main__':
    main()
