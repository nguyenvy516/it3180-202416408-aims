# Báo cáo trả lời câu hỏi thảo luận – Lab 05: Hotfix flow & bảo trì nhiều phiên bản

- **Học phần**: IT3180 – Nhập môn Công nghệ phần mềm
- **Sinh viên**: Nguyễn Thị Thảo Vy
- **MSSV**: 202416408
- **Repository**: [nguyenvy516/it3180-202416408-aims](https://github.com/nguyenvy516/it3180-202416408-aims)

---

## 1. Vì sao khi tạo nhánh `release/lab05` ở Phần A chưa gắn tag `v1.1.0`?

1. **Bản chất bất biến của Tag trong Git**:
   - Tag (đặc biệt là Annotated Tag `git tag -a`) mang ý nghĩa định danh một mốc thời gian cố định và bất biến của một baseline đã phát hành. Theo chuẩn quản lý cấu hình, **một tag đã chia sẻ/công bố thì không bao giờ được xóa hoặc di chuyển**.
2. **Giai đoạn ổn định hóa (Stabilization Phase)**:
   - Khi vừa tạo nhánh `release/lab05`, nhánh này đại diện cho ứng viên phát hành (Release Candidate). Nó cần trải qua các bước kiểm tra cuối cùng và nghiệm thu.
   - Nếu ta vội vã gắn tag `v1.1.0` ngay lập tức, khi phát hiện ra lỗi (như lỗi tìm kiếm phân biệt hoa thường ở Phần B), ta sẽ buộc phải sửa lỗi và nâng số phiên bản lên `v1.1.1` (bản vá).
   - Việc chưa gắn tag giúp ta có cơ hội tích hợp bản vá khẩn cấp thông qua cherry-pick vào nhánh `release/lab05` trước khi chính thức đóng dấu phát hành `v1.1.0`.

---

## 2. Ưu và nhược điểm của chiến lược Upstream-First so với Release-First khi xử lý Hotfix

### Chiến lược Upstream-First (Microsoft Release Flow tiêu chuẩn)
- **Cách làm**: Sửa lỗi trên nhánh `master` trước, kiểm thử hoàn chỉnh, sau đó dùng `git cherry-pick` đưa bản vá ngược về các nhánh `release/*` đang cần bảo trì.
- **Ưu điểm**:
  - Đảm bảo lỗi không bao giờ bị bỏ quên trên nhánh phát triển chính (không bị hiện tượng thoái lui lỗi - regression ở các phiên bản tương lai).
  - Tận dụng ngay pipeline CI/CD hiện đại nhất trên master.
- **Nhược điểm**:
  - Có thể bị chậm trễ: Do master đang chứa nhiều tính năng mới đang dở dang, việc merge vào master đòi hỏi phải giải quyết xung đột với những phần code mới, làm chậm thời gian phát hành bản vá khẩn cấp cho khách hàng.

### Chiến lược Release-First (Mô hình rút gọn của học phần)
- **Cách làm**: Tách nhánh `hotfix/*` từ chính nhánh `release/*` bị lỗi, sửa và kiểm thử ngay trên môi trường của bản phát hành đó, sau đó cherry-pick bản sửa về `master`.
- **Ưu điểm**:
  - Khắc phục sự cố khẩn cấp cực nhanh: Bản sửa chỉ tập trung vào mã nguồn tối thiểu của phiên bản khách hàng đang sử dụng, loại bỏ hoàn toàn các rủi ro từ những tính năng mới chưa ổn định trên master.
- **Nhược điểm**:
  - Đòi hỏi tính kỷ luật cao: Nếu lập trình viên quên lan truyền (cherry-pick) bản sửa lỗi về master, lỗi đó sẽ xuất hiện trở lại ở các phiên bản tiếp theo.

---

## 3. Nếu quên lan truyền bản sửa sang `release/lab05`, những lệnh kiểm toán nào ở Phần F sẽ phát hiện?

Trong Phần F (Kiểm toán đa phiên bản), hệ thống sử dụng các lệnh sau để phát hiện việc bỏ quên bản vá:

1. **Lệnh `git log --grep`**:
   ```bash
   git log --all --oneline --grep "cherry picked from commit <FIX_SHA>"
   ```
   - **Kỳ vọng**: Phải hiển thị đủ **2 commit cherry-pick** (1 commit trên `master` và 1 commit trên `release/lab05`).
   - **Phát hiện**: Nếu quên lan truyền sang `release/lab05`, lệnh này chỉ hiển thị duy nhất 1 commit (trên `master`).

2. **Lệnh kiểm tra tính tương đương `git cherry`**:
   ```bash
   git cherry -v origin/release/lab05 origin/release/lab04
   ```
   - Lệnh này so sánh các bản vá giữa hai nhánh. Nếu `release/lab05` chưa có bản vá tương đương của commit `<FIX_SHA>`, commit đó sẽ bị đánh dấu dấu cộng (`+`), cảnh báo thiếu sót.

3. **Script kiểm tra hành vi tự động trên cả 3 dòng phiên bản**:
   ```bash
   for ref in v1.0.1 v1.1.0 master; do
       git switch --detach -q $ref
       printf "%-8s " $ref
       python -c "from aims.dvd import DigitalVideoDisc as D; from aims.search import search_by_title; print(len(search_by_title([D('The Lion King')], 'lion')))"
   done
   git switch -q master
   ```
   - **Kỳ vọng**: Cả 3 dòng đều phải in ra `1`:
     ```
     v1.0.1   1
     v1.1.0   1
     master   1
     ```
   - **Phát hiện**: Nếu quên cherry-pick sang `release/lab05`, phiên bản `v1.1.0` sẽ in ra `0` (không tìm thấy do phân biệt hoa thường), lập tức vạch ra lỗi kiểm toán cấu hình.

---

## 4. Tách biệt giữa Commit sửa lỗi và Commit nâng phiên bản trong Hotfix

- Trong bài thực hành Lab 05, tại nhánh hotfix ta thực hiện tách làm 2 commit riêng biệt:
  - **Commit 1**: `fix: make search_by_title case-insensitive` (chỉ chứa file test và logic sửa lỗi).
  - **Commit 2**: `chore: bump version to 1.0.1` (chỉ sửa `__version__ = "1.0.1"` và ghi chú CHANGELOG).
- **Lý do SCM**:
  - Khi cần lan truyền bản sửa lỗi về `master` (đang ở phiên bản `1.1.0`), ta chỉ muốn lấy phần logic sửa code thông qua `git cherry-pick -x <FIX_SHA>`.
  - Nếu gộp cả việc đổi version vào cùng một commit, khi cherry-pick về master, nó sẽ cố gắng ghi đè version `1.0.1` lên `1.1.0`, gây ra xung đột phiên bản không đáng có. Tách rời commit giúp việc bảo trì đa phiên bản trở nên hoàn toàn module hóa và sạch sẽ.
