# Báo cáo trả lời câu hỏi thảo luận – Lab 01: Thiết lập môi trường & Refactor flow

- **Học phần**: IT3180 – Nhập môn Công nghệ phần mềm
- **Sinh viên**: Nguyễn Thị Thảo Vy
- **MSSV**: 202416408
- **Repository**: [nguyenvy516/it3180-202416408-aims](https://github.com/nguyenvy516/it3180-202416408-aims)

---

## 1. Cấu hình `--global` được lưu ở đâu? Khác gì so với `--local`?

### Vị trí lưu trữ
- **Cấu hình `--global`**: Được lưu trong file `.gitconfig` tại thư mục người dùng:
  - Trên Windows: `C:\Users\<Username>\.gitconfig` (hoặc `%USERPROFILE%\.gitconfig`).
  - Trên Linux / macOS: `~/.gitconfig` (tương đương `/home/<username>/.gitconfig`).
- **Cấu hình `--local`**: Được lưu trực tiếp trong file cấu hình riêng của repository tại đường dẫn:
  - `<thư-mục-repo>/.git/config`.

### Điểm khác biệt chính
| Tiêu chí | Cấu hình `--global` | Cấu hình `--local` |
| :--- | :--- | :--- |
| **Phạm vi tác động** | Áp dụng cho **tất cả** repository của người dùng đó trên máy tính. | Chỉ áp dụng duy nhất cho **repository hiện tại**. |
| **Độ ưu tiên** | Thấp hơn cấu hình `--local`. | Cao nhất; ghi đè lên các thiết lập tương ứng từ `--global` và `--system`. |
| **Mục đích sử dụng** | Thiết lập thông tin mặc định của cá nhân (`user.name`, `user.email`), trình soạn thảo (`core.editor`), kết thúc dòng (`core.autocrlf`). | Thiết lập thông tin riêng biệt cho một dự án cụ thể (ví dụ dùng email công ty hoặc remote credentials riêng). |

---

## 2. Vì sao nên dùng `git mv` thay vì di chuyển tệp thủ công rồi `git add`?

1. **Giữ nguyên tính liên tục của lịch sử (History Traceability)**:
   - Khi dùng `git mv <source> <dest>`, Git ghi nhận ngay lập tức thao tác di chuyển/đổi tên vào Staging Area (chỉ số đổi tên `renamed: old -> new`).
   - Nếu di chuyển thủ công bằng File Explorer/terminal thông thường, Git có thể coi đó là hai thao tác riêng biệt: xóa file cũ (`deleted`) và tạo một file mới chưa theo dõi (`untracked`). Nếu nội dung file bị chỉnh sửa đồng thời trong lúc di chuyển, Git có thể không nhận diện được quan hệ đổi tên (rename detection score < 50%), dẫn đến đứt gãy lịch sử commit.
2. **Hỗ trợ truy vết lịch sử sâu (`git log --follow`)**:
   - Thao tác `git mv` giúp lệnh `git log --follow -- <new_path>` dễ dàng duyệt ngược lại toàn bộ các commit trước khi file được chuyển vào package mới.
3. **Thao tác nhanh chóng, tránh sai sót**:
   - `git mv` thực hiện đồng thời việc di chuyển tệp trên hệ thống tập tin và cập nhật staging area của Git trong 1 bước duy nhất, tránh tình trạng quên `git rm` file cũ gây trùng lặp mã nguồn.

---

## 3. Nhánh `release/lab01` có phải là một Baseline không? Vì sao?

**Trả lời**: **CÓ**, `release/lab01` hoàn toàn là một Baseline trong quản trị cấu hình phần mềm (SCM).

### Giải thích chi tiết theo lý thuyết SCM:
1. **Định nghĩa Baseline**: Một baseline (đường cơ sở) là một phiên bản cấu hình phần mềm chính thức đã được kiểm tra, đánh giá đạt yêu cầu và được các bên liên quan thống nhất phê duyệt. Baseline đóng vai trò là cột mốc chuẩn làm nền tảng cho các chu kỳ phát triển tiếp theo và chỉ có thể được thay đổi thông qua quy trình kiểm soát thay đổi chính thức (Formal Change Control).
2. **Đối chiếu với `release/lab01`**:
   - Nhánh `release/lab01` được tách ra từ đỉnh `master` ngay sau khi tính năng tái cấu trúc (refactor package `aims/`) đã được hoàn thành, kiểm tra kết quả chạy (`python main.py` trả về đúng `63.89 $`) và merge thông qua Pull Request #1.
   - Trạng thái mã nguồn tại nhánh này đã được "đóng băng" (frozen) để bàn giao/nộp bài đánh giá cho Lab 01, không nhận thêm các commit thử nghiệm tự do. Mọi thay đổi sửa lỗi sau này sẽ phải đi qua quy trình hotfix.

---

## 4. Vì sao không nên commit thẳng vào nhánh `master` dù làm việc một mình?

Dù chỉ có một lập trình viên duy nhất thực hiện dự án, việc **không commit trực tiếp lên master** mà luôn đi qua nhánh tính năng/tái cấu trúc và Pull Request mang lại nhiều giá trị cốt lõi:

1. **Rèn luyện văn hóa và kỷ luật SCM (Configuration Management Discipline)**:
   - Hình thành thói quen tuân thủ quy trình phát triển chuyên nghiệp theo mô hình phân nhánh chuẩn (Release Flow / GitHub Flow), giúp dễ dàng hòa nhập vào môi trường làm việc nhóm và các dự án doanh nghiệp thực tế.
2. **Cô lập rủi ro (Risk Isolation)**:
   - Mọi thay đổi mã nguồn được thực hiện trên nhánh độc lập (`feature/*`, `refactor/*`, `bugfix/*`). Nhánh `master` luôn được giữ ở trạng thái ổn định và có thể triển khai/chạy thử bất cứ lúc nào ("deployable at all times"). Nếu một nhánh thử nghiệm thất bại, ta có thể dễ dàng hủy bỏ nhánh đó mà không làm bẩn lịch sử của `master`.
3. **Thực hiện tự kiểm thử và đối soát qua Pull Request**:
   - Giao diện Pull Request cho phép xem lại toàn bộ các khác biệt (diff view, files changed), phát hiện các file rác phát sinh (`__pycache__`, file `.DS_Store`, file tạm thời) trước khi gộp vào master.
4. **Tạo vết kiểm toán (Audit Trail) minh bạch**:
   - Mỗi lần tích hợp mã nguồn đều có một PR tương ứng với mô tả mục đích, các thay đổi chính và checklist nghiệm thu rõ ràng, phục vụ đắc lực cho việc tra cứu sau này.
5. **Kích hoạt tự động hóa CI/CD**:
   - Các hệ thống CI (Continuous Integration) như GitHub Actions thường được kích hoạt khi có sự kiện mở PR để chạy tự động toàn bộ bộ kiểm thử đơn vị (unit tests), đảm bảo chất lượng mã nguồn trước khi hợp nhất.
