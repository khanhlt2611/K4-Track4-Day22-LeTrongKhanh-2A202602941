"""Chạy các lượt thử ngắn và lưu nhật ký để điền báo cáo cá nhân."""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    """Chạy lần lượt hai tracker và quét từng ngưỡng, dừng nếu một lượt lỗi."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab-data-root', type=Path, default=Path('data_lab21'))
    parser.add_argument('--device', default='cuda:0')
    parser.add_argument('--max-frames', type=int, default=150)
    args = parser.parse_args()
    configs = [('bytetrack', .3, .5), ('botsort', .3, .5),
               ('botsort', .15, .5), ('botsort', .5, .5),
               ('botsort', .3, .4), ('botsort', .3, .7),
               ('bytetrack', .15, .5), ('bytetrack', .5, .5),
               ('bytetrack', .3, .4), ('bytetrack', .3, .7)]
    manifest = []
    for index in range(1, 6):
        video = f'video_{index}'
        for tracker, conf, iou in configs:
            if tracker == "bytetrack" and (conf, iou) != (.3, .5) and index not in (1, 3):
                continue
            name = f'{tracker}_conf{conf}_iou{iou}'
            out = Path('runs/thu_nghiem') / video / name
            log_file = out / 'log.txt'
            out.mkdir(parents=True, exist_ok=True)
            run_file = out / f'{video}_run.json'
            if not run_file.exists():
                command = [sys.executable, '-u', 'scripts/run_tracking.py',
                           '--source', str(args.lab_data_root / video / 'img1'),
                           '--seq-name', video, '--tracker', tracker,
                           '--conf', str(conf), '--iou', str(iou),
                           '--out', str(out), '--save-video',
                           '--max-frames', str(0 if index == 1 else args.max_frames), '--device', args.device]
                print(f'Đang thử {video}: {name}', flush=True)
                with log_file.open('w', encoding='utf-8') as log:
                    subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
            if index == 1 and not (out / 'evaluate.txt').exists():
                eval_command = [sys.executable, '-u', 'scripts/evaluate_practice.py',
                                '--trackeval-root', 'TrackEval', '--lab-data-root', str(args.lab_data_root),
                                '--submission', str(out / 'video_1.txt'), '--run-name', name]
                with (out / 'evaluate.txt').open('w', encoding='utf-8') as log:
                    subprocess.run(eval_command, stdout=log, stderr=subprocess.STDOUT, check=True)
            record = json.loads(run_file.read_text(encoding='utf-8'))
            record['output'] = str(out)
            manifest.append(record)
            Path('runs/thu_nghiem/manifest.json').write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'Xong {video}: {name}, {record["frames"]} frame', flush=True)


if __name__ == '__main__':
    main()
