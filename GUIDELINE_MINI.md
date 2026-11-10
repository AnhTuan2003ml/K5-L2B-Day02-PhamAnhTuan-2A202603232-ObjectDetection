# Mini guideline — Phạm Anh Tuấn (L2B)

## 1. Định nghĩa bốn lớp

| Class ID | Lớp | Quy tắc nhận diện trong bản nhãn hiện có |
| ---: | --- | --- |
| 0 | `car` | Ô tô con, sedan, hatchback, SUV và taxi. Trường hợp pickup nhỏ chỉ phân vào `car` khi đã đối chiếu quy ước của lớp; không mặc định mọi pickup đều là ô tô con. |
| 1 | `truck` | Xe tải chở hàng, xe tải thùng, xe đầu kéo/container và phương tiện có kết cấu xe tải. |
| 2 | `bus` | Xe buýt, xe khách và xe chở khách có cấu trúc, kích thước đặc trưng của bus. |
| 3 | `van` | Xe van/minivan có thân hộp, phục vụ chở người hoặc hàng hóa; không đồng nhất xe buýt cỡ lớn với van. |

Giữ thứ tự `car=0`, `truck=1`, `bus=2`, `van=3` theo `data.yaml`. Vật thể ngoài bốn lớp, ví dụ xe máy, xe đạp, người đi bộ, không được gán nhãn. Đối với phương tiện khó phân biệt `bus` và `van`, cần ghi lại ảnh và hỏi giảng viên trước khi quyết định cuối cùng, theo `GUIDE.md`.

## 2. Quy tắc bounding box

- Một xe thuộc phạm vi bài tập tương ứng một box; không gộp nhiều xe trong một box.
- Box bám sát phần thân xe nhìn thấy được, không bao gồm đường, nền hoặc xe khác.
- Xe bị che khuất vẫn được gán nếu có đủ bằng chứng để nhận diện lớp; box bám phần quan sát được, không suy đoán hình dạng bị che.
- Xe cắt qua rìa ảnh có box kết thúc tại mép ảnh; không kéo box ra ngoài khung.
- Với xe nhỏ, mờ hoặc dễ nhầm lớp, không quyết định theo suy đoán; ghi lại trường hợp cần đối chiếu.
- Định dạng YOLO mỗi dòng: `class_id x_center y_center width height`, tọa độ chuẩn hóa về `[0, 1]`.

## 3. Ba tình huống cần đối chiếu với file nhãn thực tế

Bảng dưới đây ghi **lớp đang có trong file nhãn**, không xác nhận đó là quyết định thủ công của học viên. Khi rà soát các ảnh `drive_002`, `drive_035` và `drive_050`, những mô tả trước đây về “pickup nhỏ” và “xe buýt đã gán `bus`” chưa khớp rõ ràng với ảnh và nhãn hiện tại; vì vậy không được coi các mô tả cũ là minh chứng đã hoàn tất self-QC.

| Ảnh | Tình huống cần kiểm tra | Lớp ghi nhận trong nhãn hiện có | Vấn đề cần học viên xác nhận |
| --- | --- | --- | --- |
| `drive_002` | Xe chở khách thân lớn ở gần giữa ảnh | Có box `van` (`3`) tại khu vực xe thân lớn | Đối chiếu `bus`/`van` và chỉ rõ đối tượng được lựa chọn, không suy diễn một pickup không có định vị rõ trong ảnh. |
| `drive_035` | Xe chở khách thân hộp ở phía trái phần đường | Có box `van` (`3`) ở khu vực xe này | Xác nhận đó là van/minivan hay bus theo schema; ghi lý do dựa trên đặc điểm thực tế. |
| `drive_050` | Xe chở khách lớn ở sát mép dưới ảnh | Có box `van` (`3`) tại khu vực xe bị cắt khung | Kiểm tra đồng thời phân lớp `bus`/`van` và cách xử lý xe cắt khung. |

**Trạng thái:** Những dòng trên là các ca kiểm tra có thật trong bộ ảnh/nhãn được cung cấp. Phần **quyết định cuối cùng và lý do do học viên tự xác nhận** vẫn cần hoàn tất; không được coi quan sát của công cụ là quyết định gán nhãn cá nhân. Không chỉnh sửa nhãn hoặc kết quả QC chỉ để khớp phần trình bày này.
