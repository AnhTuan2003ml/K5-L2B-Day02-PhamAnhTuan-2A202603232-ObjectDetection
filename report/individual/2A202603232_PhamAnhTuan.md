# Báo cáo cá nhân - Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Phạm Anh Tuấn
- MSSV: 2A202603232
- Lớp: L2B
- Email: Chưa cung cấp
- Repository: https://github.com/AnhTuan2003ml/K5-L2B-Day02-PhamAnhTuan-2A202603232-ObjectDetection
- Colab: Không có. Quá trình huấn luyện được chạy cục bộ bằng Docker với GPU NVIDIA RTX 4060. Đây là điểm chưa đúng yêu cầu nộp link Colab trong `SUBMISSION.md`.

## 2. Schema và mini guideline

- Schema bắt buộc: `car = 0`, `truck = 1`, `bus = 2`, `van = 3`, giữ nguyên trong `data.yaml`.
- Nội dung định nghĩa lớp, quy tắc vẽ box và ba ca mơ hồ được ghi tại [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md), gồm `drive_002` (pickup nhỏ xếp `car`), `drive_035` (xe compact thân hộp xếp `van`) và `drive_050` (xe khách bị che một phần xếp `bus`).
- Repo không có nhật ký hoặc commit riêng chứng minh ba quyết định trên do học viên trực tiếp thực hiện; nội dung được giữ nguyên để học viên xác nhận trước khi nộp.

## 3. Annotation và self-QC

- Số file nhãn train: 50, cùng basename với 50 ảnh trong `dataset/images/train/`.
- Kết quả chạy `python tools/check_yolo_labels.py`:

```text
ĐẠT cấu trúc: 50/50 file nhãn hợp lệ. Chờ ground truth để chấm chất lượng.
```

- Kiểm tra bổ sung: 700 box, không có dòng trùng lặp, không có dòng sai số cột/class/tọa độ; class phân bố `car = 566`, `truck = 50`, `bus = 20`, `van = 64`.
- Commit nhãn đầu tiên là `3428ae7` (commit `786fe1a` chỉ có `.gitkeep`, không có nhãn). Bộ nhãn hiện tại đang ở working tree, chưa commit.
- Nguồn nhãn: học viên cho biết đã gán lại nhãn. Trước khi dọn repo, working tree còn thư mục `ai_labels_retrain_tiled` có nội dung trùng với `dataset/labels/train`; repo cũng từng có `tools/generate_ai_labels.py`. Vì vậy chưa có bằng chứng đây là nhãn do học viên tự gán; nếu nhãn do model sinh thì vi phạm `RULES.md`.
- Self-QC thủ công: repo không có nhật ký xác minh thủ công. Danh sách cũ có `drive_060`, nhưng `drive_060` thuộc tập eval nên không được tính là ảnh train đã kiểm tra. Không thay bằng tên ảnh train khác khi chưa có bằng chứng; học viên cần bổ sung nhật ký các ảnh đã mở và kiểm tra thực tế.

## 4. Gold QC và rework

| Chỉ số | Bản nhãn trước | Bản relabel hiện tại |
|---|---:|---:|
| TP | 507 | 591 |
| FP | 183 | 109 |
| FN | 146 | 62 |
| Precision | 0.7348 | 0.8443 |
| Recall | 0.7764 | 0.9051 |
| F1 | 0.7550 | 0.8736 |
| mean IoU của matches | 0.8777 | 0.8873 |
| Đạt ngưỡng | Không | Có |

- Số liệu bản hiện tại khớp với [outputs/annotation_evaluation.json](../../outputs/annotation_evaluation.json): TP `591`, FP `109`, FN `62`, P `0.8443`, R `0.9051`, F1 `0.8736`, mean IoU `0.8873`, `passed = true`.
- Đây là chỉ số chất lượng annotation, không phải mAP của model.
- Bộ giá trị TP `429`, FP `95`, FN `224`, F1 `0.7290` là một lần thử trung gian, không phải kết quả cuối.
- Bản relabel hiện tại đạt ngưỡng annotation, nhưng chưa có bằng chứng đây là vòng sửa nhãn thủ công.

## 5. Kết quả YOLO

- Môi trường: Docker, CUDA 12.4.1, PyTorch 2.6.0+cu124, Ultralytics 8.4.0, GPU NVIDIA RTX 4060.
- Cấu hình theo [args.yaml](assets/yolo26_runs/vehicle_annotation/args.yaml): `yolo26n.pt`, dữ liệu `data.yaml` (`dataset/images/train` + `dataset/labels/train`), 50 epoch, `imgsz = 640`, `batch = -1`, `seed = 20260909`.
- Checkpoint được đánh giá: `outputs/yolo26_runs/yolo26n_student_labels/weights/best.pt`, chọn theo fitness tại epoch 49; SHA256 `b43526aa...`.
- Không dùng `dataset_gold_finetune` hoặc nhãn gold để train model này; eval chỉ dùng làm validation.

Kết quả trên 10 ảnh eval, khớp [model_eval_metrics.json](assets/yolo26_runs/model_eval_metrics.json):

| Chỉ số trên eval | Giá trị |
|---|---:|
| Precision | 0.7396 |
| Recall | 0.2181 |
| mAP50 | 0.2004 |
| mAP50-95 | 0.1388 |

Kết quả theo lớp trên eval:

| Lớp | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| car | 0.528 | 0.681 | 0.626 | 0.437 |
| truck | 1.000 | 0.000 | 0.000 | 0.000 |
| bus | 1.000 | 0.000 | 0.000 | 0.000 |
| van | 0.433 | 0.194 | 0.175 | 0.118 |

- Ảnh dự đoán trên 10 ảnh eval: [drive_051](assets/eval_predictions/visuals/drive_051.jpg), [drive_052](assets/eval_predictions/visuals/drive_052.jpg), [drive_053](assets/eval_predictions/visuals/drive_053.jpg), [drive_054](assets/eval_predictions/visuals/drive_054.jpg), [drive_055](assets/eval_predictions/visuals/drive_055.jpg), [drive_056](assets/eval_predictions/visuals/drive_056.jpg), [drive_057](assets/eval_predictions/visuals/drive_057.jpg), [drive_058](assets/eval_predictions/visuals/drive_058.jpg), [drive_059](assets/eval_predictions/visuals/drive_059.jpg), [drive_060](assets/eval_predictions/visuals/drive_060.jpg).

Trả lời bốn câu hỏi cuối notebook:

1. Trên eval, recall theo lớp: `car = 0.681`, `van = 0.194`, `truck = 0.000`, `bus = 0.000`. `truck` và `bus` thấp nhất nhưng chỉ có 5 và 2 instance, không đủ để kết luận chắc chắn.
2. mAP50 `0.2004` cao hơn mAP50-95 `0.1388`, cho thấy box lệch nhiều ở ngưỡng IoU cao; cần đối chiếu [val_batch0_pred.jpg](assets/yolo26_runs/vehicle_eval/val_batch0_pred.jpg).
3. mAP50 theo lớp: `car = 0.626`, `van = 0.175`, `truck = 0`, `bus = 0`. `truck`/`bus`/`van` có quá ít mẫu và có thể bị nhầm với `car`; cần xem [confusion_matrix.png](assets/yolo26_runs/vehicle_eval/confusion_matrix.png) để xác định cặp nhầm lẫn.
4. Không dùng eval để train vì eval là tập validation dùng chọn checkpoint và đo khả năng tổng quát hóa; đây không phải test set độc lập.

## 6. Khó khăn và cách xử lý

| Bước | Vấn đề | Cách đã thử | Kết quả |
|---|---|---|---|
| Dữ liệu | Chỉ 50 ảnh train, mất cân bằng lớp | Ghi nhận phân bố box hiện tại | `car` chiếm đa số; `bus` chỉ có 20 box |
| Nhãn | Bản nhãn trước F1 `0.7550` | Gán lại và đánh giá lại với gold | F1 `0.8736`, đạt ngưỡng annotation |
| Nguồn nhãn | Chưa có nhật ký gán thủ công | Kiểm tra working tree trước khi dọn | Từng có `ai_labels_retrain_tiled`; chưa chứng minh được nhãn thủ công |
| Huấn luyện | Cần model mới từ nhãn hiện tại | Train `yolo26n.pt` trên `dataset/labels/train`, val trên eval | mAP50 `0.2004`, mAP50-95 `0.1388` |
| Thử nghiệm cũ | Từng fine-tune trên gold | Không dùng làm kết quả nộp | Kết quả gold-finetuned bị leakage, đã loại khỏi báo cáo |
| Môi trường | Image Docker đổi tag | Dùng image `cvat.pytorch.ultralytics.yolo26m:latest` | Chạy được train/val cục bộ |
| Nộp bài | Yêu cầu link Colab | Không chạy Colab | Thiếu minh chứng Colab theo `SUBMISSION.md` |

## 7. Tự đánh giá theo rubric

- Định dạng YOLO: đạt 50/50 file, 5 cột, tọa độ chuẩn hóa, class ID đúng.
- Đầy đủ vật thể, độ bám sát và phân lớp: chưa xác minh được bằng kiểm tra thủ công có minh chứng; nguồn nhãn chưa được xác nhận là thủ công.
- Mini guideline: file có định nghĩa lớp, quy tắc box và ba ca mơ hồ; chưa có bằng chứng các quyết định do học viên tự đưa ra.
- Gold-set QC: F1 `0.8736` đạt `0.80`; mean IoU `0.8873` đạt `0.70`.
- Pipeline YOLO: có log, metrics và ảnh eval, nhưng không có Colab.
- Kết quả model trên eval: mAP50 `0.2004`, mAP50-95 `0.1388`; thấp do 50 ảnh, mất cân bằng lớp và model nhỏ.
- Kết luận: bài chưa tuân thủ đầy đủ `SUBMISSION.md` (thiếu Colab) và chưa có minh chứng nhãn do học viên tự gán; không nên nộp ở trạng thái hiện tại.

## 8. Công cụ AI và tài liệu tham khảo

- AI được dùng để hỗ trợ chạy train/eval bằng Docker, kiểm tra artifact và soạn báo cáo. Nhãn từng được sinh bởi model (thư mục `ai_labels_retrain_tiled` và script `tools/generate_ai_labels.py` trong lịch sử); nếu dùng nhãn AI để nộp thì vi phạm `RULES.md`.
- Ultralytics 8.4.0 (train/val/predict), checkpoint pretrained `yolo26n.pt`.
- Tài liệu bài lab: `RULES.md`, `SUBMISSION.md`, `RUBRIC.md`, `GUIDE.md`.
