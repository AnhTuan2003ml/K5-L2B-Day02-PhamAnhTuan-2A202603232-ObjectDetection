# Báo cáo cá nhân — Ngày 2: Object Detection

## 1. Thông tin học viên

- **Họ tên:** Phạm Anh Tuấn
- **MSSV:** 2A202603232
- **Lớp:** L2B
- **Repository:** https://github.com/AnhTuan2003ml/K5-L2B-Day02-PhamAnhTuan-2A202603232-ObjectDetection
- **Môi trường chạy YOLO:** máy local, Docker, GPU NVIDIA RTX 4060; **không có phiên Colab hoặc link Colab đã chạy** trong hồ sơ.
- **Minh chứng chạy local:** [tham số huấn luyện](assets/yolo26_runs/vehicle_annotation/args.yaml), [log theo epoch](assets/yolo26_runs/vehicle_annotation/results.csv), [kết quả đánh giá](assets/yolo26_runs/model_eval_metrics.json).

**Về hình thức thực hiện:** Ultralytics/YOLO26 có thể train và evaluate trên máy local, không bắt buộc phải dùng Colab về mặt kỹ thuật. Các kết quả dưới đây là kết quả local đã lưu, không được mô tả thành kết quả Colab. Tuy nhiên, `SUBMISSION.md` và `RUBRIC.md` gốc yêu cầu notebook/link Colab; **việc chấp nhận minh chứng local thay thế là quyết định của giảng viên**, không thể tự xác nhận trong báo cáo. Tên repository hiện có chữ `Day02`, khác quy ước `DAY02` trong `SUBMISSION.md`.

## 2. Schema và mini guideline

Schema bốn lớp trong [data.yaml](../../data.yaml): `car = 0`, `truck = 1`, `bus = 2`, `van = 3`; không sửa thứ tự class. Định nghĩa lớp và quy tắc box được tập hợp tại [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md), theo nguyên tắc: mỗi phương tiện một box, chỉ ôm phần quan sát được, xử lý xe bị che/cắt khung mà không tự đoán phần khuất.

Ba ảnh được nêu để rà các tình huống phân biệt `bus`/`van` và xử lý xe lớn là `drive_002`, `drive_035`, `drive_050`. Đối chiếu ảnh và nhãn hiện có cho thấy các vị trí xe chở khách thân lớn đang có box lớp `van`. Các mô tả cũ về pickup nhỏ hoặc xe đã được gán `bus` không thể dùng làm bằng chứng quyết định chính xác. **Học viên cần tự xác nhận vật thể, lớp cuối cùng và lý do cho từng ca**; bản biên tập không sửa nhãn để hợp thức hóa guideline.

## 3. Annotation và self-QC

Bộ dữ liệu train gồm **50 ảnh** và **50 file nhãn** cùng basename trong `dataset/labels/train/`. Lệnh đã chạy:

```text
python tools/check_yolo_labels.py
ĐẠT cấu trúc: 50/50 file nhãn hợp lệ. Chờ ground truth để chấm chất lượng.
```

Kiểm tra định dạng độc lập: **656 box**, phân bố `car = 464`, `truck = 27`, `bus = 90`, `van = 75`; không có dòng trùng lặp hoặc sai số cột/class/tọa độ. Kiểm tra cấu trúc không thay thế đánh giá về tính đầy đủ, phân lớp và độ sát box.

Commit đầu tiên có nhãn là `3428ae7`; commit `786fe1a` chỉ có `.gitkeep` (đã đối chiếu `git log`).

**Nguồn nhãn:** học viên đã gán nhãn 50 ảnh train và gán lại nhãn 10 ảnh val/eval; không dùng AI để sinh nhãn. Nhãn đã được kiểm tra cấu trúc bằng checker. Repo chưa có nhật ký self-QC chi tiết từng ảnh.

## 4. Annotation QC và tập val

- `gold_train_labels` bị gán nhãn sai (ví dụ xe buýt bị gán thành `van`/`truck`), nên được loại khỏi huấn luyện và đánh giá.
- Học viên đã gán nhãn tập train và gán lại nhãn tập val/eval.
- Tập val gồm 10 ảnh `drive_051`–`drive_060`, đã được gán lại nhãn. Nhãn val hiện có **127 box**: `car = 102`, `truck = 4`, `bus = 12`, `van = 9`.
- Val chỉ dùng để validation/chọn `best.pt` trong huấn luyện; **không đưa ảnh val vào train**.
- Không có đối chiếu gold/F1 trong báo cáo này.

## 5. Pipeline và kết quả YOLO26 trên local

**Thông số phiên đã lưu:** checkpoint khởi tạo `yolo26n.pt`, huấn luyện tối đa **300 epoch** với early stopping (`patience = 50`), dừng ở epoch 209, **best epoch 159**; `imgsz = 640`, `batch = -1`, `device = 0`, `seed = 20260909`; train trên `dataset/images/train` (50 ảnh, không oversample), validation trên `dataset/images/eval` (nhãn val đã gán lại); run `yolo26n_train_early`. Tham số trong [args.yaml](assets/yolo26_runs/vehicle_annotation/args.yaml), log trong [results.csv](assets/yolo26_runs/vehicle_annotation/results.csv). Checkpoint `best.pt` có SHA256 bắt đầu bằng `341e7037` và **không đưa vào GitHub**.

Kết quả trên 10 ảnh val, khớp [model_eval_metrics.json](assets/yolo26_runs/model_eval_metrics.json):

| Chỉ số | Kết quả trên 10 ảnh val |
| --- | ---: |
| Precision | **0.5831** |
| Recall | **0.3999** |
| mAP50 | **0.4221** |
| mAP50–95 | **0.3337** |

Kết quả theo lớp trên val:

| Lớp | P | R | mAP50 | mAP50–95 |
| --- | ---: | ---: | ---: | ---: |
| car | 0.689 | 0.631 | 0.671 | 0.587 |
| truck | 0.370 | 0.250 | 0.279 | 0.119 |
| bus | 0.611 | 0.500 | 0.548 | 0.443 |
| van | 0.641 | 0.222 | 0.187 | 0.180 |

**Ảnh dự đoán trên toàn bộ 10 ảnh val:** [051](assets/eval_predictions/visuals/drive_051.jpg) · [052](assets/eval_predictions/visuals/drive_052.jpg) · [053](assets/eval_predictions/visuals/drive_053.jpg) · [054](assets/eval_predictions/visuals/drive_054.jpg) · [055](assets/eval_predictions/visuals/drive_055.jpg) · [056](assets/eval_predictions/visuals/drive_056.jpg) · [057](assets/eval_predictions/visuals/drive_057.jpg) · [058](assets/eval_predictions/visuals/drive_058.jpg) · [059](assets/eval_predictions/visuals/drive_059.jpg) · [060](assets/eval_predictions/visuals/drive_060.jpg).

**Phân tích từ các minh chứng đã lưu:**

1. **Lớp có recall thấp:** trên val, recall theo lớp là `car = 0.631`, `bus = 0.500`, `truck = 0.250`, `van = 0.222`. `van` và `truck` thấp nhất nhưng chỉ có 9 và 4 instance; `bus` có 12 instance và đã cải thiện nhờ train dài hơn.
2. **mAP50 và mAP50–95:** mAP50 `0.4221` cao hơn mAP50–95 `0.3337`. Khi yêu cầu IoU chặt hơn, khả năng ghép prediction với nhãn giảm; cần đối chiếu [val_batch0_pred.jpg](assets/yolo26_runs/vehicle_eval/val_batch0_pred.jpg).
3. **Ví dụ lỗi/độ phủ:** mAP50 theo lớp là `car = 0.671`, `bus = 0.548`, `truck = 0.279`, `van = 0.187`. `drive_052` vẫn bị bỏ sót ở `conf=0.25`, cho thấy model còn hạn chế với bus lớn/bị che.
4. **Không dùng val để train:** val chỉ dùng để validation/chọn checkpoint; đây không phải test set độc lập.

Phân bố đối tượng trong tập train là `464 car`, `27 truck`, `90 bus`, `75 van` (50 ảnh, 656 box); không dùng oversample và không đưa val vào train.

## 6. Khó khăn và cách xử lý

| Nội dung | Ghi nhận thực tế | Trạng thái |
| --- | --- | --- |
| Định dạng nhãn | 50/50 file qua checker; 656 box train | Đã kiểm tra cấu trúc |
| Nhãn val | Gán lại 10 ảnh val; 127 box | Đã dùng cho validation |
| Huấn luyện | Run local `yolo26n_train_early` trên Docker/GPU; early stopping 300 epoch/patience 50; best epoch 159 | Có minh chứng thực thi local |
| Đánh giá val | P `0.5831`, R `0.3999`, mAP50 `0.4221`, mAP50–95 `0.3337` | Có file minh chứng |
| Bus trên val | mAP50 `0.548`, recall `0.500` | Cải thiện so với 50 epoch; `drive_052` vẫn sót |
| Self-QC và các ca mơ hồ | Chưa có nhật ký xác nhận thủ công của học viên | Cần học viên bổ sung |
| Hình thức nộp | Không có link Colab; có kết quả local | Cần giảng viên xác nhận chấp nhận thay thế |

## 7. Tự đánh giá theo rubric

- **Định dạng YOLO:** đạt yêu cầu kiểm tra cấu trúc (50/50 file, lớp/tọa độ hợp lệ).
- **Đầy đủ vật thể, hình học box, phân lớp:** chưa thể xác nhận chỉ từ checker; cần kiểm chứng thủ công và xác minh nguồn nhãn.
- **Mini guideline:** có định nghĩa lớp, quy tắc box và ba ảnh cần đối chiếu; quyết định cuối và lý do do học viên đưa ra chưa có xác nhận đủ tin cậy.
- **Annotation QC:** không dùng gold; tập val đã được gán lại và dùng làm validation.
- **Pipeline:** có log và 10 ảnh val từ local; **chưa đáp ứng nguyên văn mục link Colab của đề gốc**, trừ khi giảng viên cho phép local thay thế.
- **Kết quả model:** val mAP50 `0.4221`, mAP50–95 `0.3337`; `bus` mAP50 `0.548`, `car` `0.671`.
- **Kết luận:** các file minh chứng kỹ thuật đã có nhưng còn thiếu xác nhận cá nhân về self-QC/guideline; chưa nên tuyên bố đạt toàn bộ rubric.

## 8. Công cụ AI và tài liệu tham khảo

- **Ultralytics/YOLO26n:** công cụ huấn luyện, đánh giá và dự đoán trên local, theo log được cung cấp.
- **AI hỗ trợ biên tập/kiểm tra tài liệu:** được sử dụng để rà đường dẫn, đối chiếu số liệu và biên tập nội dung báo cáo; phần này không thay thế xác nhận cá nhân về annotation, self-QC hay quyết định mơ hồ.
- **Nguồn gốc nhãn:** nhãn train do học viên gán; nhãn val/eval do học viên gán lại; không dùng AI để sinh nhãn.
- **Tài liệu bài tập:** [RULES.md](../../RULES.md), [GUIDE.md](../../GUIDE.md), [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md), [SUBMISSION.md](../../SUBMISSION.md).
