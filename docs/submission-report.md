# BÁO CÁO TỔNG KẾT BÀI TẬP THỰC HÀNH SCM (IT3180)
## QUẢN LÝ CẤU HÌNH PHẦN MỀM VỚI GIT & GITHUB

---

### THÔNG TIN SINH VIÊN
- **Họ và tên**: Nguyễn Thị Thảo Vy
- **Mã số sinh viên (MSSV)**: 202416408
- **Email sinh viên**: vy.ntt2416408@sis.hust.edu.vn
- **Tài khoản GitHub**: nguyenvy516
- **Repository chính thức**: [https://github.com/nguyenvy516/it3180-202416408-aims](https://github.com/nguyenvy516/it3180-202416408-aims)

---

### 1. TỔNG QUAN HỆ THỐNG & QUY TRÌNH ÁP DỤNG
Bài thực hành áp dụng đầy đủ quy trình **Release Flow** rút gọn của học phần IT3180 đối với dự án mẫu **AIMS-mini**, mô phỏng các hoạt động quản lý cấu hình phần mềm (SCM) theo chuẩn công nghiệp:
- **Identification (Định danh cấu hình)**: Quản lý cấu hình qua commit SHA, cây thư mục, quy ước Conventional Commits, `.gitignore`, `.gitattributes`.
- **Change Control (Kiểm soát thay đổi)**: Kiểm soát qua nhánh riêng biệt (`refactor/*`, `feature/*`, `bugfix/*`, `topic/*`, `hotfix/*`), Pull Request có mô tả theo template, review & approve.
- **Status Accounting (Ghi nhận trạng thái)**: Sử dụng Semantic Versioning (`1.0.0`, `1.0.1`, `1.1.0`), duy trì file `CHANGELOG.md` theo chuẩn Keep a Changelog, so sánh bằng `git log A..B`, `git describe`.
- **Configuration Audit (Kiểm toán cấu hình)**: Quản lý baseline qua Annotated Tags (`v0.1.0` - `v1.1.0`), kiểm thử đa phiên bản bằng `git switch --detach` và matrix testing script.
- **Release Management (Quản lý phát hành)**: Đóng băng các nhánh phát hành `release/labXX`, phát hành hotfix bằng kỹ thuật `cherry-pick -x` độc lập, tích hợp tự động hóa Continuous Integration với GitHub Actions.

---

### 2. BẢNG TỔNG HỢP CÁC NHÁNH VÀ TAGS

#### Danh sách nhánh (Branches)
| Tên nhánh | Mục đích | Base từ |
| :--- | :--- | :--- |
| `master` | Nhánh tích hợp chính (Source of Truth) của toàn bộ dự án | - |
| `release/lab01` | Baseline nộp bài cho Lab 01 (Tái cấu trúc mã nguồn vào package `aims/`) | `master` |
| `release/lab02` | Baseline nộp bài cho Lab 02 (Hoàn thiện `print_cart`, `search_by_title`, PR template) | `master` |
| `release/lab03` | Baseline nộp bài cho Lab 03 (Sửa lỗi giới hạn giỏ hàng, giảm giá, giải quyết xung đột) | `master` |
| `release/lab04` | Dòng bảo trì phiên bản phát hành `1.0.x` (đã nhận hotfix `1.0.1`) | `master` |
| `release/lab05` | Dòng phát hành phiên bản `1.1.0` (đã nhận hotfix và tính năng mở rộng) | `master` |

#### Danh sách Thẻ phiên bản (Annotated Tags)
| Thẻ (Tag) | Trỏ tới nhánh | Phiên bản | Nội dung đánh dấu |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | `release/lab01` | 0.1.0 | Bản phát hành hoàn thành Lab 01 (Refactor package) |
| `v0.2.0` | `release/lab02` | 0.2.0 | Bản phát hành hoàn thành Lab 02 (Feature & Review flow) |
| `v0.3.0` | `release/lab03` | 0.3.0 | Bản phát hành hoàn thành Lab 03 (Bugfix & Conflict flow) |
| `v1.0.0` | `release/lab04` | 1.0.0 | Bản phát hành chính thức đầu tiên (Production Baseline) |
| `v1.0.1` | `release/lab04` | 1.0.1 | Bản vá lỗi tìm kiếm không phân biệt hoa thường trên dòng 1.0.x |
| `v1.1.0` | `release/lab05` | 1.1.0 | Bản phát hành nâng cấp tính năng mới và đồng bộ bản vá |

---

### 3. MINH CHỨNG CHECKLIST ĐẠT ĐƯỢC THEO 5 BÀI LAB

#### Lab 01 – Thiết lập môi trường & Refactor flow
- [x] Repository có cấu trúc package chuẩn: `aims/` (`__init__.py`, `cart.py`, `dvd.py`), file thực thi `main.py` ở thư mục gốc.
- [x] Tệp `.gitignore` hoạt động tốt: Không có thư mục `__pycache__/` hoặc file tạm lọt vào kho mã nguồn.
- [x] PR #1 đã được tạo và merge vào `master`, nhánh tạm đã được xóa.
- [x] Nhánh nộp bài `release/lab01` đã được tạo và gắn tag `v0.1.0`.
- [x] File trả lời câu hỏi thảo luận: `docs/answers-lab01.md`.
- [x] Kiểm tra chạy demo: `python main.py` in đúng `Total cost: 63.89 $`.

#### Lab 02 – Feature/Topic flow & Pull Request
- [x] Có mẫu Pull Request Template chuẩn tại `.github/pull_request_template.md`.
- [x] Đã áp dụng quy trình Code Review (yêu cầu sửa đổi khi giỏ hàng trống và cập nhật lại).
- [x] Thể hiện đủ 3 kiểu tích hợp merge trên đồ thị Git:
  - **Merge commit** (`--no-ff`): Áp dụng cho tính năng in giỏ hàng `feature/cart-print`.
  - **Squash and merge**: Áp dụng cho tính năng tìm kiếm `feature/search-by-title`.
  - **Rebase and merge**: Áp dụng cho tài liệu ca sử dụng `topic/use-case-diagram`.
- [x] Tạo nhánh `release/lab02`, gắn tag `v0.2.0` và file trả lời `docs/answers-lab02.md`.

#### Lab 03 – Bugfix flow, xung đột & hoàn tác
- [x] Ghi nhận lỗi giỏ hàng chấp nhận đĩa thứ 21 (Issue #6).
- [x] Áp dụng quy trình kiểm thử hồi quy: Viết test tái hiện lỗi trong `tests/test_cart.py` và chứng minh FAIL trước khi sửa code.
- [x] Sửa điều kiện giới hạn giỏ hàng: `if len(self.items) >= MAX_NUMBERS_ORDERED:` và commit với thông điệp `Fixes #6`.
- [x] Triển khai tính năng giảm giá `total_cost_with_discount` và xử lý kiểm tra ngoại lệ `ValueError`.
- [x] Xử lý xung đột mã nguồn (Merge Conflict) và cam kết thông báo hợp nhất: `print(f"Đã thêm đĩa '{dvd.title}' vào giỏ hàng")`.
- [x] Tạo nhánh `release/lab03`, gắn tag `v0.3.0` và file trả lời `docs/answers-lab03.md`.

#### Lab 04 – Release flow & Phiên bản phát hành
- [x] Chuẩn bị phát hành đúng quy trình trên master: Cập nhật `CHANGELOG.md` theo chuẩn Keep a Changelog và bump version `__version__ = "1.0.0"`.
- [x] Tách nhánh phát hành `release/lab04`, gắn annotated tag `v1.0.0`.
- [x] Nhánh `release/lab04` tuyệt đối không merge ngược vào master.
- [x] Tiếp tục phát triển tính năng mới trên master (`sort_by_title`, `sort_by_cost` trong `Cart`) mà không làm ảnh hưởng bản phát hành `1.0.0`.
- [x] Gắn các tag `v0.1.0`, `v0.2.0`, `v0.3.0` cho các bản phát hành cũ.
- [x] File trả lời câu hỏi thảo luận: `docs/answers-lab04.md`.

#### Lab 05 – Hotfix flow & Bảo trì nhiều phiên bản
- [x] Tách nhánh `release/lab05` từ master cho bản phát hành `1.1.0`.
- [x] Tiếp nhận lỗi tìm kiếm phân biệt hoa thường (Issue #20).
- [x] Tạo nhánh `hotfix/search-case-insensitive` từ nhánh phát hành `release/lab04`:
  - Tách commit 1 (chỉ sửa code + test) để lấy mã `<FIX_SHA>`.
  - Tách commit 2 (bump version lên `1.0.1` cho dòng 1.0.x).
  - Gắn tag `v1.0.1` trên nhánh `release/lab04`.
- [x] Dùng `git cherry-pick -x <FIX_SHA>` để lan truyền bản sửa lỗi về `master` và về `release/lab05`.
- [x] Gắn tag `v1.1.0` trên `release/lab05`.
- [x] Tích hợp workflow CI tự động của GitHub Actions trong `.github/workflows/ci.yml`.
- [x] Chạy kiểm thử thành công trên toàn bộ 3 dòng phiên bản (`v1.0.1`, `v1.1.0`, `master`).
- [x] File trả lời câu hỏi thảo luận: `docs/answers-lab05.md`.

---

### 4. KẾT QUẢ KIỂM THỬ HỆ THỐNG
1. **Chạy kiểm thử đơn vị tự động**:
   ```bash
   python -m unittest discover -s tests -v
   ```
   *Kết quả*: **Ran 8 tests in 0.002s - OK** (100% tests đạt yêu cầu).
2. **Chạy ứng dụng mẫu**:
   ```bash
   python main.py
   ```
   *Kết quả*:
   ```
   AIMS-mini v1.1.0
   Đã thêm đĩa 'The Lion King' vào giỏ hàng
   Đã thêm đĩa 'Star Wars' vào giỏ hàng
   Đã thêm đĩa 'Aladdin' vào giỏ hàng
   Total cost: 63.89 $

   ***********************CART***********************
   Ordered Items:
   1. DVD - The Lion King - Animation - Roger Allers - 87: 19.95 $
   2. DVD - Star Wars - Science Fiction - George Lucas - 87: 24.95 $
   3. DVD - Aladdin - Animation -  - 0: 18.99 $
   Total cost: 63.89 $
   ***************************************************
   ```
