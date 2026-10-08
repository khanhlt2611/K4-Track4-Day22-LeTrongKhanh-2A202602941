# Lab Tracking — 2 giờ

Nhóm 2 người một máy. Detector đã khóa. Bạn chọn tracker và ngưỡng cho năm video khác cảnh.

## Việc cần làm

1. Tạo môi trường một lần:

```bash
conda env create -f environment.yml
conda activate cv_robotics_lab21
git clone https://github.com/JonathonLuiten/TrackEval.git
pip install -e TrackEval/
```

2. Tải ảnh năm video: [data_lab21.zip](https://drive.google.com/file/d/1UeVPQd6j5pSzxoJDcKJrerT9SL3vJLDt/view?usp=sharing). Giải nén, rồi gán đường dẫn thư mục chứa `video_1` … `video_5`:

```bash
export LAB_DATA=/đường/dẫn/lab_data
python scripts/check_data.py --lab-data-root "$LAB_DATA"
```

Cả năm video phải có ảnh. Chỉ `video_1` có nhãn.

3. Mở `on_tap_metrics.ipynb` bằng kernel env này. Đọc bảng MOTA / IDF1 / HOTA, rồi chạy YOLO trên một ảnh `video_1`.

4. Chạy tracker. Bản thử có thể giới hạn frame. Bản nộp thì không.

```bash
python scripts/run_tracking.py \
  --source "$LAB_DATA/video_1/img1" \
  --seq-name video_1 \
  --tracker bytetrack --conf 0.3 --iou 0.5 \
  --out runs/nop_bai --save-video
```

Đổi `--seq-name` và thư mục `img1` cho `video_2` … `video_5`. Tracker được chọn: `bytetrack`, `ocsort`, `botsort`, `strongsort`, `deepocsort`.

5. Chấm số **chỉ** `video_1`:

```bash
python scripts/evaluate_practice.py \
  --trackeval-root ~/TrackEval \
  --lab-data-root "$LAB_DATA" \
  --submission runs/nop_bai/video_1.txt \
  --run-name nhom01_video1
```

`video_2` đến `video_5` không có nhãn. Xem `preview/video_N.mp4` và video có vẽ ID, rồi ghi điều bạn thấy.

## Luật chơi

| Khóa | Bạn chọn |
|---|---|
| Detector `yolo26n.pt`, ảnh 640 px, lớp người, Re-ID `osnet_x0_25_msmt17.pt` | Tracker, `--conf`, `--iou` của detector |

## Nộp

- `video_1.txt` … `video_5.txt` trong `runs/nop_bai/` (đủ frame, đúng tên).
- `submission_template/BAO_CAO_mau.md` đã điền. Số HOTA / MOTA / IDF1 chỉ bắt buộc cho `video_1`.

Chi tiết từng bước, sự cố, và lịch 2 giờ: [HUONG_DAN.md](HUONG_DAN.md).

## Chạy trên Windows PowerShell và làm cá nhân

Trong PowerShell, thay lệnh `export` bằng:

```powershell
$env:LAB_DATA = "$PWD\data_lab21"
python scripts/check_data.py --lab-data-root "$env:LAB_DATA"
```

Dùng `$env:LAB_DATA` trong các lệnh tiếp theo và viết lệnh trên một dòng (hoặc nối dòng bằng dấu backtick của PowerShell). Bài cá nhân vẫn thực hiện đủ năm video; ghi một thành viên trong báo cáo.

Môi trường Python 3.11 dùng BoxMOT 10.0.84 và OpenCV 4.11.0.86 vì BoxMOT 10.0.42 khóa NumPy 1.23.1 không tương thích bộ thư viện của lab. Các trọng số và kích thước ảnh vẫn giữ theo đề. Script đọc ảnh hỗ trợ đường dẫn tiếng Việt và xuất thêm `video_N_run.json` ghi số frame thực sự đã xử lý. Nếu gói dữ liệu thiếu `eval_config.json`, script dùng tên chấm nội bộ `LAB`, nhánh `train`; vẫn chỉ chấm nhãn của `video_1`.

## Bài cá nhân đã hoàn thành

Báo cáo đã điền: [BAO_CAO_LeTrongKhanh.md](submission_template/BAO_CAO_LeTrongKhanh.md). Xem [NOP_BAI.md](NOP_BAI.md) để tìm bộ ZIP, kết quả và lệnh chạy lại.
