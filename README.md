# Module Quản Lý Tài Sản – Odoo (odoo-fitdnu)

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

---

## 1. Giới thiệu

**Module Quản Lý Tài Sản (odoo-fitdnu)** là module mở rộng được phát triển trên nền tảng **Odoo 15**, nhằm cung cấp giải pháp **quản lý tài sản toàn diện cho doanh nghiệp**, đặc biệt phù hợp với các doanh nghiệp vừa và nhỏ (SME).

Module này được **nâng cấp và mở rộng** từ đề tài **TTDN-15-04-N6**, bổ sung thêm nhiều nghiệp vụ thực tế, tích hợp sâu với **kế toán và nhân sự**, đồng thời cải tiến kiến trúc và giao diện.

---

## 2. Phạm vi và chức năng chính

Module hỗ trợ quản lý toàn bộ vòng đời của tài sản, bao gồm:

- Dashboard tổng quan tài sản và tình hình mượn trả
- Quản lý loại tài sản
- Quản lý tài sản cụ thể
- Phân bổ tài sản cho phòng ban / nhân viên
- Tính khấu hao tài sản tự động
- Kiểm kê tài sản định kỳ
- Luân chuyển tài sản
- Thanh lý tài sản
- Quản lý đơn mượn – trả và cấp phát tài sản

### Một số giao diện tiêu biểu

- Dashboard tổng quan  
- Quản lý mượn trả tài sản  
- Quản lý loại tài sản  
- Tài sản cụ thể  
- Phân bổ – luân chuyển – thanh lý  
- Kiểm kê và khấu hao tài sản  

(Các hình ảnh minh họa được lưu trong thư mục `images/`)

---

## 3. Điểm nổi bật của module

- Quản lý tài sản theo **quy trình nghiệp vụ thực tế**
- Tính khấu hao tự động theo nhiều phương pháp
- Theo dõi lịch sử sử dụng, bảo trì và luân chuyển
- Dashboard trực quan, hỗ trợ ra quyết định nhanh
- Workflow rõ ràng, phân trạng thái nghiệp vụ
- Dễ mở rộng và tích hợp thêm module khác

---

## 4. Nâng cấp so với đề tài TTDN-15-04-N6

So với phiên bản gốc **TTDN-15-04-N6**, module đã được nâng cấp và cải tiến đáng kể:

- ✅ **Bổ sung module kế toán tài sản**
  - Tự động tạo bút toán khấu hao
  - Quản lý tài khoản tài sản và chi phí

- ✅ **Mở rộng nghiệp vụ tài sản**
  - Lịch sử bảo trì tài sản
  - Chi tiết kiểm kê và xử lý chênh lệch
  - Phân bổ và luân chuyển nâng cao

- ✅ **Khấu hao tự động**
  - Hỗ trợ nhiều phương pháp khấu hao
  - Tính toán định kỳ theo tháng

- ✅ **Tích hợp nhân sự**
  - Gắn tài sản với phòng ban và nhân viên
  - Quản lý mượn/trả theo người dùng

- ✅ **Cải tiến giao diện & Dashboard**
  - Dashboard tổng quan trực quan
  - Biểu đồ và thống kê nhanh

- ✅ **Tài liệu và hướng dẫn**
  - README chi tiết
  - Hướng dẫn cài đặt và sử dụng

---

## 5. Yêu cầu hệ thống

- Ubuntu 20.04+
- Python 3.8+
- PostgreSQL
- Docker & Docker Compose
- Odoo 15

---

## 6. Cài đặt và chạy hệ thống

### 6.1. Clone project

```bash
git clone https://github.com/antruong2004/TTDN-16-05-N8.git
cd TTDN-16-05-N8
