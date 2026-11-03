# Báo cáo trả lời câu hỏi thảo luận – Lab 02: Feature/Topic flow & Pull Request

- **Học phần**: IT3180 – Nhập môn Công nghệ phần mềm
- **Sinh viên**: Nguyễn Thị Thảo Vy
- **MSSV**: 202416408
- **Repository**: [nguyenvy516/it3180-202416408-aims](https://github.com/nguyenvy516/it3180-202416408-aims)

---

## 1. Vì sao phải đồng bộ nhánh với `master` trước khi gửi hoặc merge Pull Request?

1. **Tích hợp sớm để phát hiện xung đột (Early Integration & Conflict Detection)**:
   - Trong quá trình lập trình viên phát triển tính năng trên nhánh riêng, nhánh `master` có thể đã nhận thêm các commit/tính năng mới từ các thành viên khác.
   - Bằng cách đồng bộ (`git merge origin/master` hoặc `git rebase origin/master`), lập trình viên sẽ phát hiện và giải quyết xung đột cục bộ ngay tại máy mình thay vì đẩy gánh nặng xử lý xung đột lên reviewer hoặc làm hỏng quá trình tích hợp.
2. **Kiểm tra tính tương thích và hồi quy (Regression Testing)**:
   - Sau khi đồng bộ, lập trình viên có thể chạy lại bộ kiểm thử (`python -m unittest discover -s tests -v`) và chương trình chính (`python main.py`) để chắc chắn rằng code mới không làm hỏng tính năng sẵn có trên master.
3. **Đảm bảo PR ở trạng thái sẵn sàng tích hợp (Clean Mergeable State)**:
   - Giúp GitHub hiển thị trạng thái "Able to merge" màu xanh lá, reviewer có thể tự tin phê duyệt và bấm merge mà không gặp thông báo "This branch has conflicts".

---

## 2. Khi nào không được dùng rebase? Giải thích quy tắc vàng của Rebase

### Quy tắc vàng của Rebase (The Golden Rule of Rebasing)
> **"Không bao giờ rebase một nhánh công khai (public branch) đã được push lên remote hoặc có người khác cùng tham gia phát triển."**

### Chi tiết và Hậu quả:
- **Cơ chế rebase**: `git rebase` tua lại các commit trên nhánh hiện tại và tạo ra các commit hoàn toàn mới (cùng nội dung thay đổi nhưng mang **mã băm SHA mới** và mốc thời gian mới) đặt tiếp nối vào đỉnh nhánh gốc.
- **Hậu quả nếu vi phạm**:
  - Khi một nhánh đã chia sẻ bị rebase và `push --force`, toàn bộ các lập trình viên khác đang theo dõi nhánh đó sẽ bị phân kỳ lịch sử (diverged branch).
  - Khi họ thực hiện `git pull`, Git sẽ hiểu nhầm các commit cũ là commit mới cần gộp, tạo ra vô số commit trùng lặp, xung đột phức tạp ("Merge Hell") và phá hủy tính toàn vẹn của lịch sử dự án.
- **Khi nào NÊN dùng rebase**:
  - Chỉ dùng trên các nhánh cá nhân riêng biệt (private feature branch) tại máy local trước khi tạo PR, nhằm làm sạch và tuyến tính hóa lịch sử commit cá nhân.

---

## 3. Nhánh `feature/*` khác `topic/*` ra sao?

| Đặc điểm | Nhánh `feature/*` | Nhánh `topic/*` |
| :--- | :--- | :--- |
| **Mục đích** | Phát triển một chức năng nghiệp vụ cụ thể của phần mềm (người dùng trực tiếp trải nghiệm). | Thực hiện một nhiệm vụ ngắn hạn, phi nghiệp vụ, công việc tổ chức dự án hoặc thử nghiệm. |
| **Phạm vi thay đổi** | Mã nguồn ứng dụng và các bộ kiểm thử đơn vị đi kèm. | Cấu hình dự án, bổ sung tài liệu, workflow CI, thêm template PR/Issue, chuẩn bị phát hành. |
| **Thời gian tồn tại** | Trung bình (từ vài giờ đến vài ngày cho một tính năng). | Thường rất ngắn (short-lived, chỉ qua 1-2 commit để hoàn thành một nhiệm vụ cụ thể). |
| **Ví dụ trong học phần** | `feature/cart-print`, `feature/search-by-title`, `feature/sort-cart`. | `topic/pr-template`, `topic/use-case-diagram`, `topic/prepare-release-1.0.0`. |

---

## 4. So sánh 3 kiểu merge trên GitHub

| Tiêu chí | Merge commit (`--no-ff`) | Squash and merge | Rebase and merge |
| :--- | :--- | :--- | :--- |
| **Cơ chế hoạt động** | Tạo một merge commit mới có 2 nhánh cha, bảo lưu toàn bộ các commit con. | Gộp toàn bộ commit trên nhánh thành **1 commit duy nhất** rồi áp dụng lên master. | Tái áp dụng từng commit riêng rẽ của nhánh tiếp nối đỉnh master (SHA mới). |
| **Lịch sử Git (Graph)** | Lịch sử dạng đồ thị rẽ nhánh và hợp nhất (Non-linear). | Lịch sử tuyến tính (Linear), chỉ thêm 1 commit tóm tắt. | Lịch sử hoàn toàn tuyến tính (Linear), giữ nguyên số lượng commit. |
| **Bảo lưu chi tiết** | **Tốt nhất**: Giữ nguyên mọi mốc commit con, thời gian và tác giả. | **Thấp**: Các commit nhỏ lẻ trong quá trình làm việc bị nén lại thành 1. | **Trung bình**: Giữ nguyên từng bước nhưng thay đổi mã băm SHA. |
| **Khả năng hoàn tác (Revert)** | Rất dễ: Dùng 1 lệnh `git revert -m 1 <sha>` để đảo ngược toàn bộ tính năng. | Rất dễ: Dùng 1 lệnh `git revert <sha>` vì tính năng chỉ gồm 1 commit. | Phức tạp: Phải revert thủ công từng commit đơn lẻ cấu thành nên tính năng. |
| **Trường hợp khuyên dùng** | Các tính năng lớn, quan trọng, cần theo dõi toàn bộ tiến trình phát triển và kiểm toán. | Các tính năng nhỏ, các PR có nhiều commit vụn vặt ("fix typo", "wip", "debug"). | Các nhánh có chuỗi commit được chau chuốt kỹ càng, cần giữ lịch sử thẳng tắp không có merge commit. |
