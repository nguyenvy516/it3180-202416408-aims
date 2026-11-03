# Báo cáo trả lời câu hỏi thảo luận – Lab 04: Release flow & phiên bản phát hành

- **Học phần**: IT3180 – Nhập môn Công nghệ phần mềm
- **Sinh viên**: Nguyễn Thị Thảo Vy
- **MSSV**: 202416408
- **Repository**: [nguyenvy516/it3180-202416408-aims](https://github.com/nguyenvy516/it3180-202416408-aims)

---

## 1. Vì sao chuẩn bị phát hành trên `master` trước, không sửa trên nhánh release?

1. **Nguyên tắc "Master là nguồn chân lý duy nhất" (Single Source of Truth)**:
   - Các công việc chuẩn bị phát hành như cập nhật số phiên bản (`__version__ = "1.0.0"`), đồng bộ `main.py` và ghi nhận lịch sử thay đổi `CHANGELOG.md` là các hoạt động tích hợp cấu hình chính thức của dự án.
   - Khi chuẩn bị trực tiếp trên `master`, toàn bộ tài liệu và mã nguồn chuẩn bị phát hành đều được trải qua quy trình review và kiểm thử tự động của master.
2. **Tuân thủ nguyên tắc một chiều của Release Flow**:
   - Trong mô hình Release Flow, nhánh `release/*` chỉ nhận mã nguồn từ `master` và **tuyệt đối không merge ngược về master**.
   - Nếu thực hiện sửa tài liệu hoặc bump version trực tiếp trên nhánh release, những thay đổi này sẽ bị cô lập trên nhánh release đó. Để đưa về master, ta sẽ phải cherry-pick hoặc tìm cách merge ngược, gây phát sinh nguy cơ xung đột không cần thiết. Do đó, chuẩn bị trên master rồi rẽ nhánh release là giải pháp tối ưu và sạch sẽ nhất.

---

## 2. Vì sao nhánh `release/*` không bao giờ merge ngược vào `master`?

1. **Tránh "Merge Hell" và xung đột cấu trúc**:
   - Nhánh `master` liên tục tiến lên phía trước với các tính năng mới của các phiên bản tiếp theo (ví dụ Lab 05 phát triển tiếp tính năng `sort-cart` và `search-by-category`).
   - Nếu merge ngược một nhánh `release/lab04` cũ vào `master`, ta có thể vô tình đưa những cấu hình cũ hoặc mã nguồn chưa nâng cấp đè lên tiến trình mới của master, dẫn tới xung đột phức tạp.
2. **Bảo toàn tính toàn vẹn của bản phát hành (Frozen Baseline)**:
   - Nhánh release đại diện cho một bản phân phối ổn định được đóng băng tại một thời điểm. Mối quan hệ giữa master và release là quan hệ phân nhánh phục vụ bảo trì riêng rẽ.
   - Nếu có lỗi phát sinh trên bản release, lỗi sẽ được sửa bằng nhánh hotfix chuyên biệt và chỉ lan truyền về master thông qua **cherry-pick có chọn lọc** (`git cherry-pick -x <FIX_SHA>`), chứ không merge ồ ạt cả nhánh release vào master.

---

## 3. So sánh mô hình Release Flow với GitFlow

| Tiêu chí | Release Flow (học phần / Microsoft) | GitFlow |
| :--- | :--- | :--- |
| **Nhánh chính vĩnh viễn** | Duy nhất **1 nhánh** chính: `master`. | Có **2 nhánh** vĩnh viễn song song: `main` (production) và `develop` (phát triển). |
| **Điểm rẽ nhánh tính năng** | Tách từ `master` và merge trực tiếp vào `master`. | Tách từ `develop` và merge vào `develop`. |
| **Tạo nhánh release** | Tách trực tiếp từ `master` khi sẵn sàng đóng băng baseline. | Tách từ `develop` khi chuẩn bị phát hành. |
| **Hoàn tất phát hành** | Nhánh release được giữ lại để bảo trì/nộp bài, **không merge ngược**. | Phải **merge kép** vào cả `main` lẫn `develop`, sau đó xóa nhánh release. |
| **Xử lý Hotfix** | Tạo nhánh hotfix từ bản release cần vá, sau đó dùng `cherry-pick -x` đưa bản sửa về master. | Tạo nhánh hotfix từ `main`, sau đó merge kép vào cả `main` lẫn `develop`. |
| **Độ phức tạp** | **Đơn giản, tinh gọn**, phù hợp với chu kỳ phát triển nhanh và CI/CD hiện đại. | **Phức tạp, cồng kềnh**, dễ xảy ra xung đột khi develop và main bị lệch pha thời gian dài. |

---

## 4. Vì sao tăng phiên bản lên `1.0.0` mà không phải `0.4.0`?

Theo đặc tả của **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):
1. **Giai đoạn tiền phát hành (`0.y.z`)**:
   - Được sử dụng trong các Lab 01, 02, 03 (`v0.1.0` -> `v0.3.0`). Đây là giai đoạn thử nghiệm ban đầu (initial development), kiến trúc và API chưa ổn định, có thể thay đổi bất kỳ lúc nào.
2. **Cột mốc phiên bản chính thức (`1.0.0`)**:
   - Tại Lab 04, ứng dụng AIMS-mini đã hoàn thiện đầy đủ các chức năng cốt lõi: cấu trúc gói hoàn chỉnh (`aims/`), quản lý giỏ hàng (`add`, `remove`, `total_cost`, `print_cart`), tìm kiếm DVD theo tiêu đề (`search_by_title`), cơ chế giảm giá, xử lý lỗi tràn giỏ hàng và có bộ unit tests tự động hoàn chỉnh.
   - Việc nâng lên `1.0.0` tuyên bố sản phẩm đã đạt mức độ sẵn sàng sản xuất (Production-Ready) với API ổn định và cam kết tương thích ngược theo tiêu chuẩn SemVer.

---

## 5. Ý nghĩa của Status Accounting và Configuration Audit trong SCM

- **Status Accounting (Ghi nhận trạng thái)**:
  - Trả lời câu hỏi: *"Hệ thống hiện tại đang ở trạng thái nào so với các phiên bản trước?"*
  - Công cụ: `git log A..B`, `git describe --tags`, `CHANGELOG.md`. Giúp lập trình viên và người quản lý biết chính xác có những commit nào mới, sự khác biệt giữa hai bản phát hành.
- **Configuration Audit (Kiểm toán cấu hình)**:
  - Trả lời câu hỏi: *"Bản phát hành có đúng là những gì đã được thống nhất và có tái tạo lại chính xác được không?"*
  - Công cụ: `git tag -n`, `git switch --detach`, `git worktree`, chạy test tự động trên tag phát hành. Đảm bảo bản phát hành không bị lẫn tệp rác, pass 100% kiểm thử và có thể khôi phục lại bất kỳ lúc nào.
