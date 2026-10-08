"""Kiểm tra định dạng và số frame đã chạy của năm file nộp."""
import argparse
import json
import math
from pathlib import Path
from typing import Iterable


def validate_rows(rows: Iterable[str], n_frames: int) -> int:
    """Kiểm tra các dòng kết quả và trả về số hộp hợp lệ.

    Args:
        rows: Các dòng theo định dạng mười cột của lab.
        n_frames: Số frame của video nguồn.

    Returns:
        Số dòng kết quả không rỗng.

    Raises:
        ValueError: Khi sai định dạng, trùng ID trong frame hoặc không có kết quả.
    """
    seen = set()
    count = 0
    for line_number, line in enumerate(rows, 1):
        if not line.strip():
            continue
        fields = line.strip().split(',')
        if len(fields) != 10:
            raise ValueError(f'Dòng {line_number}: cần đúng 10 cột')
        values = [float(value) for value in fields]
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f'Dòng {line_number}: có giá trị không hữu hạn')
        frame, track_id = values[:2]
        if frame != int(frame) or not 1 <= frame <= n_frames:
            raise ValueError(f'Dòng {line_number}: frame ngoài video')
        if track_id != int(track_id) or track_id < 0:
            raise ValueError(f'Dòng {line_number}: ID không hợp lệ')
        if values[4] <= 0 or values[5] <= 0 or not 0 <= values[6] <= 1:
            raise ValueError(f'Dòng {line_number}: hộp hoặc confidence không hợp lệ')
        key = (int(frame), int(track_id))
        if key in seen:
            raise ValueError(f'Dòng {line_number}: trùng ID trong một frame')
        seen.add(key)
        count += 1
    if count == 0:
        raise ValueError('File kết quả rỗng')
    return count


def main() -> None:
    """Đối chiếu dữ liệu nguồn, nhật ký chạy và năm file kết quả."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab-data-root', type=Path, default=Path('data_lab21'))
    parser.add_argument('--submission', type=Path, default=Path('runs/nop_bai'))
    args = parser.parse_args()
    summary = []
    for index in range(1, 6):
        video = f'video_{index}'
        expected = len(list((args.lab_data_root / video / 'img1').glob('*.jpg')))
        metadata = json.loads((args.submission / f'{video}_run.json').read_text(encoding='utf-8'))
        if expected == 0 or metadata['frames'] != expected or metadata['max_frames'] != 0:
            raise ValueError(f'{video}: chưa chạy đủ frame nguồn')
        if metadata['detector'] != 'yolo26n.pt' or metadata['imgsz'] != 640:
            raise ValueError(f'{video}: sai detector hoặc kích thước ảnh của đề')
        count = validate_rows((args.submission / f'{video}.txt').read_text().splitlines(), expected)
        summary.append({'video': video, 'frames': expected, 'rows': count, 'status': 'OK'})
        print(f'{video}: OK, {expected} frame đã xử lý, {count} dòng hợp lệ')
    (args.submission / 'kiem_tra_ban_nop.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
