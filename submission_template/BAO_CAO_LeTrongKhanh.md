# Báo cáo lab: chọn tracker cho 5 video

**Hình thức:** Cá nhân  
**Thành viên:** Lê Trọng Khánh  
**Mã học viên:** 2A202602941

Detector cố định: `yolo26n.pt`, ảnh 640 px, chỉ lớp người. Các lượt BoT-SORT dùng cùng trọng số Re-ID `osnet_x0_25_msmt17.pt`. Không huấn luyện hoặc đổi trọng số, không chỉnh tham số nội bộ tracker và không thêm nhãn cho bốn video không có nhãn.

## 1. Cấu hình đã chọn

| Video | Tracker | conf | iou | Quan sát khi xem các khung hình có ID | Đã thử nhưng loại |
|---|---|---:|---:|---|---|
| video_1 | bytetrack | 0.15 | 0.5 | Người áo tím giữ ID 3 tại frame 60/100/140 và vẫn ID 3 tại frame 300; nhiều người nhỏ ở xa chưa được theo dõi. | botsort, conf=0.3, iou=0.5: HOTA và IDF1 thấp hơn; ByteTrack conf=0.5 cũng làm metric giảm. |
| video_2 | botsort | 0.15 | 0.5 | Người áo trắng bên trái gần cột đèn giữ ID 8 ở frame 60/100/140; người áo xám bên phải giữ ID 4 ở các frame 50/525/1030 của bản đầy đủ. Nhóm đông phía trên vẫn có người không có hộp. | bytetrack, conf=0.3, iou=0.5: người áo trắng chưa có ID ở frame 60 và nhận ID 16 ở frame 100; botsort conf=0.5 bỏ nhiều hộp hơn ở đoạn mẫu. |
| video_3 | bytetrack | 0.3 | 0.5 | Ba người gần camera giữ ID 1/2/24 ở frame 60/100/140; một người xa giữ ID 31 tại frame 100/140. Ảnh nhỏ và camera di chuyển vẫn làm hộp người xa kém ổn định. | botsort, conf=0.3, iou=0.5: người xa cạnh người áo sọc đổi từ ID 29 ở frame 100 sang 33 ở frame 140. ByteTrack conf=0.15/0.5 không cho ưu thế rõ ở các ảnh mẫu. |
| video_4 | botsort | 0.3 | 0.5 | Người áo đỏ giữ ID 2 và người áo trắng giữ ID 5 tại frame 60/100/140; áo đỏ còn ID 2 tại frame 450 nhưng thành ID 88 tại frame 880. Phản chiếu vẫn sinh hộp. | botsort conf=0.5: ở frame 140, ID 2 chuyển sang người áo đen phía sau; bytetrack còn đổi ID ở hình phản chiếu. |
| video_5 | botsort | 0.3 | 0.5 | Người áo đỏ bên phải giữ ID 2 ở frame 60/100/140; người áo xám phía sau giữ ID 11 tại frame 60/100. Người xa và vùng tối bị bỏ sót nhiều. | bytetrack, conf=0.3, iou=0.5: người áo xám từ ID 15 ở frame 60 thành 23 tại frame 100; botsort conf=0.15 cũng đổi từ 11 sang 20 trong đoạn này. |

## 2. Số liệu video_1

Chấm đúng `runs/nop_bai/video_1.txt` bằng `scripts/evaluate_practice.py`, tên lần chấm `LeTrongKhanh_video1`. Các số bên dưới do TrackEval xuất, theo thang 0–100 cho ba metric chính:

| HOTA | MOTA | IDF1 | TP | FN | FP | Đổi ID |
|---:|---:|---:|---:|---:|---:|---:|
| 27.316 | 18.314 | 26.987 | 3534 | 15047 | 118 | 13 |

Đầu ra tóm tắt từ lần chấm cuối:

```text
HOTA:     video_1  HOTA=27.316  DetA=15.857  AssA=47.148
CLEAR:    video_1  MOTA=18.314  TP=3534  FN=15047  FP=118  IDSW=13
Identity: video_1  IDF1=26.987  IDR=16.146  IDP=82.147
Count:    video_1  Dets=3652  GT_Dets=18581  IDs=35  GT_IDs=62
```

Bản log đầy đủ nằm ở `metrics_video_1.txt` trong bộ nộp. Số dòng file gốc có thể lớn hơn Dets trong bảng chấm vì TrackEval loại dự đoán khớp các nhãn thuộc diện không chấm trong bước tiền xử lý. Không có số HOTA/MOTA/IDF1 cho video_2–video_5.

### So sánh các cấu hình video_1 trên đủ 600 frame

| Tracker | conf | iou | HOTA | MOTA | IDF1 | Đổi ID |
|---|---:|---:|---:|---:|---:|---:|
| bytetrack | 0.3 | 0.5 | 26.917 | 17.297 | 25.712 | 12 |
| botsort | 0.3 | 0.5 | 23.148 | 17.055 | 20.74 | 34 |
| botsort | 0.15 | 0.5 | 23.333 | 17.932 | 21.778 | 34 |
| botsort | 0.5 | 0.5 | 23.331 | 15.828 | 20.581 | 30 |
| botsort | 0.3 | 0.4 | 23.147 | 17.05 | 20.741 | 34 |
| botsort | 0.3 | 0.7 | 23.18 | 17.05 | 20.761 | 34 |
| bytetrack | 0.15 | 0.5 | 27.316 | 18.314 | 26.987 | 13 |
| bytetrack | 0.5 | 0.5 | 25.276 | 15.86 | 23.439 | 14 |
| bytetrack | 0.3 | 0.4 | 26.918 | 17.297 | 25.714 | 12 |
| bytetrack | 0.3 | 0.7 | 26.021 | 17.227 | 24.844 | 13 |

ByteTrack conf=0.15, iou=0.5 có HOTA cao nhất trong các cấu hình đã thử và IDF1 cũng cao hơn baseline. So với ByteTrack conf=0.3, số bỏ sót giảm từ 15248 xuống 15047 nhưng FP tăng từ 107 lên 118 và số đổi ID tăng từ 12 lên 13. Vì vậy cấu hình cuối là một đánh đổi, không phải tốt hơn trên mọi tiêu chí. MOTA vẫn thấp vì lỗi bỏ sót chiếm phần lớn; không thể xem kết quả này là theo dõi tốt toàn bộ người trong cảnh.

## 3. Phân tích theo cảnh

### video_1 — camera tĩnh, ban ngày

ByteTrack giữ tốt ID của người áo tím trong các khung hình đã đối chiếu, còn BoT-SORT conf=0.15 chuyển người này sang ID 17 ở frame 140. Camera tĩnh và các chuyển động liên tục giúp ghép hộp bằng chuyển động có hiệu quả trong đoạn này. Số liệu đủ 600 frame ủng hộ lựa chọn ByteTrack: HOTA 27.316 và IDF1 26.987 cao hơn các cấu hình BoT-SORT đã thử. Hạ conf giúp giữ thêm đầu vào cho tracker nhưng vẫn chưa giải quyết được nhiều người nhỏ, tối hoặc bị che ở phía xa.

### video_2 — phố đêm đông người

Trong đoạn mẫu, BoT-SORT conf=0.15 duy trì ID 8 cho người áo trắng đang đi gần vùng đèn sáng, còn cấu hình conf=0.3 không vẽ người này tại frame 60. Ngoại hình có thể hỗ trợ ghép người sau che khuất trong cảnh đông, nhưng ánh sáng và kích thước người vẫn ảnh hưởng detector. Người áo xám bên phải giữ ID 4 ở cả ba khung hình đầu/giữa/cuối đã kiểm tra của bản đầy đủ. Nhóm người phía trên ảnh vẫn có nhiều trường hợp không được vẽ hộp, nên quan sát này chỉ xác nhận một số track cụ thể, không chứng minh ưu thế trên toàn video.

### video_3 — ảnh nhỏ, camera di chuyển

Ba người gần camera giữ ID 1/2/24 trong cả ba khung hình 60/100/140 với ByteTrack conf=0.3. Một người nhỏ ở phía xa giữ ID 31 tại frame 100/140, trong khi BoT-SORT đổi ID ở người tương ứng. Ảnh thấp và mờ làm thông tin ngoại hình khó dùng; thêm Re-ID không tự động giúp kết quả tốt hơn. Giữ conf=0.3 vì các lượt 0.15/0.5 chưa thể hiện cải thiện rõ qua ảnh mẫu, và không có nhãn để kết luận bằng metric.

### video_4 — camera tiến tới, kính phản chiếu

BoT-SORT conf=0.3 giữ các ID chính ở đoạn đầu và tránh việc ID 2 chuyển sang người phía sau như lượt conf=0.5 tại frame 140. Chuyển động camera và các giao cắt khiến việc ghép hộp khó hơn, nên thông tin ngoại hình là một nguồn bổ sung có ích trong đoạn thử. Tuy nhiên người áo đỏ đổi từ ID 2 ở frame 450 sang 88 ở frame 880, cho thấy Re-ID vẫn không giữ được danh tính suốt cả video. Hộp trên ảnh phản chiếu là lỗi đầu vào detector mà tracker có thể tiếp tục duy trì; không nên coi track phản chiếu ổn định là kết quả đúng.

### video_5 — quay từ xe, người nhỏ ở xa

BoT-SORT conf=0.3 giữ người áo đỏ bên phải với ID 2 trong đoạn thử và giữ người áo xám với ID 11 ở frame 60/100. Cùng người áo xám này đổi ID với ByteTrack conf=0.3 và BoT-SORT conf=0.15, nên giảm conf không luôn làm giữ ID tốt hơn. Chuyển động camera thay đổi vị trí và tỷ lệ người nhanh, trong khi ảnh người ở xa cung cấp ít thông tin. Ở frame 730 của bản đầy đủ chỉ có một hộp dù vẫn thấy những người khác, gồm người đang băng qua đường; hạn chế bỏ sót vẫn rõ.

## 4. Cách thực hiện và kiểm tra

Đã thực hiện 38 lượt so sánh: 10 cấu hình trên video_1, 10 trên video_3 và 6 trên mỗi video còn lại. Mỗi video đều có ít nhất một tracker theo chuyển động và một tracker có Re-ID. Với mỗi lượt quét, chỉ thay một ngưỡng so với cấu hình gốc conf=0.3, iou=0.5; thử conf=0.15/0.3/0.5 và iou=0.4/0.5/0.7. Các lượt video_1 chạy đủ 600 frame để chấm công bằng; bốn video còn lại thử trên 150 frame đầu rồi chạy cấu hình cuối trên toàn bộ ảnh.

Việc kiểm tra bằng mắt dùng các khung hình có ID tại 60/100/140 để so sánh cùng thời điểm và thêm các khung hình đầu/giữa/cuối của bản đầy đủ. Đây là kiểm tra mẫu khung hình, không phải xem liên tục mọi frame; các nhận xét chỉ giới hạn ở những track được nêu. Video preview đầy đủ được giữ ở `runs/nop_bai` để có thể xem lại.

Tất cả bản nộp dùng thư mục ảnh `img1`, không giới hạn frame. Bộ kiểm tra đối chiếu số ảnh nguồn với nhật ký chạy và xác nhận mỗi dòng đủ 10 cột, giá trị hữu hạn, kích thước hộp hợp lệ, frame nằm trong video và không trùng ID trong cùng frame:

| Video | Frame nguồn và đã chạy | Dòng kết quả hợp lệ |
|---|---:|---:|
| video_1 | 600 | 3751 |
| video_2 | 1050 | 10639 |
| video_3 | 837 | 4273 |
| video_4 | 900 | 5787 |
| video_5 | 750 | 2145 |

Đã chạy notebook ôn tập: ba câu trả lời True/False/True đều đúng; các ô YOLO một frame và thay conf đã chạy và có đầu ra. Bộ unit test dùng ảnh và dòng dữ liệu giả, không dùng GPU hoặc nhãn lab.

### Môi trường và sửa lỗi chạy

Dùng Python 3.11, PyTorch 2.2.2 CUDA 11.8, torchvision 0.17.2, NumPy 1.26.4, Ultralytics 8.4.174, BoxMOT 10.0.84 và OpenCV 4.11.0.86 trên RTX 3060 Laptop. Repo ban đầu khóa BoxMOT 10.0.42 với NumPy 1.23.1 gây xung đột trên Python 3.11; đã chuyển sang bản 10.0.84 của cùng dòng thư viện. Giữ setuptools dưới 81 vì BoxMOT cần pkg_resources. Các trọng số và kích thước ảnh của đề vẫn giữ nguyên.

Đã sửa đọc ảnh ở đường dẫn tiếng Việt, đưa detector lên thiết bị được chọn, ghi số frame thực sự xử lý và giới hạn pytest vào test của lab. Gói dữ liệu thiếu eval_config.json nên phần chấm dùng tên nội bộ LAB, nhánh train; nhãn video_1 và tiền xử lý lớp người của TrackEval vẫn được sử dụng. Bản vá alias NumPy được áp dụng trong chính tiến trình con chạy TrackEval.

### Chạy lại từ thư mục gốc trong PowerShell

```powershell
conda activate cv_robotics_lab21
$env:PYTHONUTF8 = "1"
$env:LAB_DATA = "$PWD\data_lab21"
python scripts/check_data.py --lab-data-root "$env:LAB_DATA"
python scripts/run_submission.py --lab-data-root "$env:LAB_DATA" --device cuda:0
python scripts/validate_submission.py --lab-data-root "$env:LAB_DATA"
python scripts/evaluate_practice.py --trackeval-root TrackEval --lab-data-root "$env:LAB_DATA" --submission runs/nop_bai/video_1.txt --run-name LeTrongKhanh_video1
pytest
```

Muốn tạo bản chạy mới, truyền `--out runs/chay_lai` cho run_submission.py và dùng đường dẫn đó khi kiểm tra hoặc chấm. Các file kết quả, nhật ký và video xem lại đã có trong `runs/nop_bai`. Không commit dữ liệu ảnh, video preview hoặc trọng số.

## 5. Nếu có thêm thời gian

Sẽ kiểm tra kỹ các frame quanh thời điểm đổi ID của người áo đỏ ở video_4 và mở rộng đoạn thử sang giữa/cuối của bốn video không có nhãn. Có thể thử các tracker còn lại trong danh sách của đề và quét conf mịn hơn; mọi mở rộng thay trọng số hoặc Re-ID phải tách khỏi bài nộp chính.
