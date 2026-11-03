# Báo cáo trả lời câu hỏi thảo luận – Lab 03: Bugfix flow, xung đột & hoàn tác

- **Học phần**: IT3180 – Nhập môn Công nghệ phần mềm
- **Sinh viên**: Nguyễn Thị Thảo Vy
- **MSSV**: 202416408
- **Repository**: [nguyenvy516/it3180-202416408-aims](https://github.com/nguyenvy516/it3180-202416408-aims)

---

## 1. Merge base là gì? Git xác định merge base như thế nào trong giải quyết xung đột?

### Định nghĩa Merge Base
- **Merge Base** là commit tổ tiên chung gần nhất (Lowest Common Ancestor - LCA) của hai nhánh chuẩn bị được hợp nhất với nhau trong đồ thị có hướng không chu trình (DAG) của Git.

### Vai trò của Merge Base trong thuật toán 3-Way Merge
Khi ta gộp nhánh `feature` vào nhánh `master`, Git không chỉ so sánh hai commit đỉnh (`HEAD` của master và `HEAD` của feature) mà thực hiện so sánh 3 chiều (**Three-Way Merge**) giữa 3 đối tượng:
1. Bản ghi tại commit **Merge Base** ($B$)
2. Bản ghi tại commit đỉnh của nhánh hiện tại ($M$)
3. Bản ghi tại commit đỉnh của nhánh cần gộp ($F$)

### Cơ chế phát hiện xung đột:
- Nếu một dòng code không thay đổi giữa $B$ và $M$, nhưng thay đổi ở $F$: Git tự động áp dụng thay đổi từ $F$.
- Nếu một dòng code không thay đổi giữa $B$ và $F$, nhưng thay đổi ở $M$: Git tự động giữ nguyên thay đổi từ $M$.
- **Nếu cùng một dòng code (hoặc vùng code liền kề) bị sửa đổi khác nhau ở CẢ $M$ LẪN $F$ so với tổ tiên chung $B$**: Git không thể tự phán đoán ý định của lập trình viên và sẽ đánh dấu **Merge Conflict**, chèn các nhãn phân tách `<<<<<<<`, `=======`, `>>>>>>>` để con người tự hòa giải.

---

## 2. Vì sao trên các nhánh chia sẻ như `master` và `release/*` phải dùng `revert` thay vì `reset`?

1. **Bảo vệ tính toàn vẹn của lịch sử công khai (Append-only History)**:
   - Lệnh `git reset` (đặc biệt là `--hard`) làm dịch chuyển con trỏ nhánh lùi về quá khứ, xóa bỏ các commit đứng sau con trỏ. Nếu các commit này đã được chia sẻ lên remote (`master`, `release/*`), việc reset sẽ buộc người dùng phải sử dụng `git push --force`.
   - `push --force` phá hủy lịch sử commit trên máy của tất cả các cộng tác viên khác, làm mất tính đồng bộ và có nguy cơ xóa nhầm công sức của người khác.
2. **Cơ chế hoạt động an toàn của `git revert`**:
   - `git revert` không xóa commit cũ. Thay vào đó, nó tính toán sự thay đổi nghịch đảo (inverse diff) và tạo ra một **commit mới** để triệt tiêu tác động của commit sai sót.
   - Nhờ đó, lịch sử commit luôn tiến về phía trước (tiếp tục nối dài), an toàn tuyệt đối cho mọi thành viên trong nhóm và đáp ứng tiêu chuẩn kiểm toán phần mềm (audit trail).
3. **Tuân thủ chính sách bảo vệ nhánh (Branch Protection Rules)**:
   - Nhánh `master` và `release/*` thường có quy tắc chặn `force push`. Do đó, `git revert` thông qua Pull Request là con đường chuẩn duy nhất được hệ thống chấp nhận.

---

## 3. Phân biệt 3 chế độ của `git reset` và cơ chế của `git reflog`

### Phân biệt 3 chế độ `git reset`
| Chế độ | Vị trí HEAD | Staging Area (Index) | Working Directory | Ngữ cảnh sử dụng điển hình |
| :--- | :--- | :--- | :--- | :--- |
| **`--soft`** | Lùi về commit chỉ định | **Giữ nguyên** các thay đổi đã staged | **Giữ nguyên** toàn bộ code | Muốn gộp nhiều commit gần nhất thành một commit mới hoặc viết lại commit message. |
| **`--mixed`** *(mặc định)* | Lùi về commit chỉ định | **Bỏ staged** (unstage tất cả thay đổi) | **Giữ nguyên** toàn bộ code chưa staged | Muốn sắp xếp lại các file cần add vào commit một cách cẩn thận hơn. |
| **`--hard`** | Lùi về commit chỉ định | **Xóa sạch** | **Xóa sạch**, khôi phục nguyên trạng commit cũ | Muốn hủy bỏ hoàn toàn những thử nghiệm thất bại và quay về trạng thái ổn định trước đó. |

### Cơ chế cứu hộ của `git reflog`
- `git reflog` (Reference Logs) là một cuốn nhật ký ghi chép lại mọi sự thay đổi của con trỏ `HEAD` trên máy cục bộ (mỗi khi commit, checkout, switch, rebase, merge, reset).
- Khi lỡ tay dùng `git reset --hard` làm mất commit quan trọng, commit đó thực tế vẫn tồn tại trong object database của Git và chưa bị bộ thu gom rác (garbage collection) dọn dẹp.
- Lập trình viên chỉ cần chạy `git reflog` để tìm lại mã SHA của commit trước khi reset, sau đó khôi phục lại bằng: `git switch -c rescue-branch <SHA_da_mat>`.

---

## 4. Tầm quan trọng của Regression Test trong quy trình sửa lỗi (Bugfix Flow)

- Trong Lab 03, trước khi sửa logic giới hạn giỏ hàng (`MAX_NUMBERS_ORDERED`), ta bắt buộc phải viết bài test tái hiện lỗi (`test_add_dvd_until_full`) và chứng minh nó bị **FAIL** trước:
  ```
  FAIL: test_add_dvd_until_full ... AssertionError: True is not false
  ```
- Ý nghĩa:
  1. **Xác nhận nguyên nhân gốc rễ**: Chứng minh bài test đã phản ánh đúng lỗi mô tả trong Issue #6.
  2. **Trở thành bài kiểm thử hồi quy (Regression Test)**: Sau khi sửa code thành công và test PASS, bài test này được lưu trữ vĩnh viễn trong bộ test suite của dự án. Trong các chu kỳ phát triển tương lai, nếu có ai vô tình làm xuất hiện lại lỗi này, bộ kiểm thử CI sẽ lập tức cảnh báo, ngăn ngừa lỗi tái phát.
