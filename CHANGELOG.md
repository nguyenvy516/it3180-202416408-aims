# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-03
### Added
- Phương thức `Cart.print_cart()` để in thông tin chi tiết các đĩa trong giỏ hàng và xử lý giỏ hàng trống.
- Hàm `search_by_title()` tìm kiếm đĩa DVD theo từ khóa tiêu đề.
- Phương thức `Cart.total_cost_with_discount(percent)` hỗ trợ tính chiết khấu giỏ hàng và kiểm tra tính hợp lệ của phần trăm chiết khấu.
- Khởi tạo tài liệu dự án: `docs/use-case.md` và mẫu Pull Request template.

### Fixed
- Giới hạn giỏ hàng: Từ chối thêm đĩa thứ 21 khi số đĩa đạt `MAX_NUMBERS_ORDERED` (20 đĩa) (#6).

### Changed
- Tái cấu trúc (Refactor): Di chuyển các module mã nguồn vào package `aims/` (`aims/dvd.py`, `aims/cart.py`, `aims/__init__.py`).
