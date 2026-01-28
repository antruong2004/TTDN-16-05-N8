# Module Quản Lý Nhân Sự

Module quản lý nhân sự toàn diện cho Odoo 15 với đầy đủ các chức năng:

## Tính năng chính

### 1. Quản lý Phòng ban (phong_ban)
- Mã phòng ban, tên phòng ban
- Cấu trúc phòng ban cha - con
- Trưởng phòng
- Thống kê số nhân viên theo phòng ban

### 2. Quản lý Chức vụ (chuc_vu)
- Mã chức vụ, tên chức vụ
- Cấp bậc chức vụ
- Lương cơ bản theo chức vụ
- Phụ cấp chức vụ
- Thống kê số nhân viên theo chức vụ

### 3. Quản lý Nhân viên (nhan_vien)
- Thông tin cá nhân: Mã NV, họ tên, giới tính, ngày sinh, địa chỉ
- Thông tin liên hệ: Email, số điện thoại
- Thông tin công việc: Phòng ban, chức vụ, ngày vào làm, trạng thái
- Thông tin bổ sung: CMND/CCCD, số BHXH, tài khoản ngân hàng
- Tự động tính tuổi và số năm công tác

### 4. Chấm công (cham_cong)
- Chấm công hàng ngày với giờ vào, giờ ra
- Tự động tính số giờ làm việc
- Phát hiện đi trễ, về sớm tự động
- Quản lý các loại công: Bình thường, nghỉ phép, nghỉ ốm, công tác, nghỉ lễ
- Ghi nhận giờ tăng ca
- Chức năng check-in/check-out cho nhân viên

### 5. Báo cáo chấm công tháng (bao_cao_cham_cong)
- Tổng hợp chấm công theo tháng
- Thống kê: Tổng ngày công, ngày đi trễ, ngày về sớm
- Thống kê nghỉ phép, nghỉ không phép
- Tổng giờ làm việc và giờ tăng ca

### 6. Bảng lương (bang_luong)
- Tính lương theo tháng cho từng nhân viên
- Lương cơ bản và các khoản phụ cấp:
  - Phụ cấp chức vụ
  - Phụ cấp ăn trua
  - Phụ cấp xăng xe
  - Phụ cấp điện thoại
  - Phụ cấp khác
- Tính tiền tăng ca tự động (hệ số 1.5)
- Tiền thưởng
- Khấu trừ tự động:
  - BHXH (8%)
  - BHYT (1.5%)
  - BHTN (1%)
  - Thuế TNCN
  - Các khoản khấu trừ khác
- Quy trình duyệt lương: Nhập → Chờ duyệt → Đã duyệt → Đã chi trả
- Tích hợp chatter để theo dõi lịch sử thay đổi

## Cấu trúc Module

```
nhan_su/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── phong_ban.py          # Model phòng ban
│   ├── chuc_vu.py            # Model chức vụ
│   ├── nhan_vien.py          # Model nhân viên
│   ├── cham_cong.py          # Model chấm công & báo cáo
│   └── bang_luong.py         # Model bảng lương
├── views/
│   ├── phong_ban_views.xml
│   ├── chuc_vu_views.xml
│   ├── nhan_vien.xml
│   ├── cham_cong_views.xml   # Views chấm công
│   ├── bang_luong_views.xml  # Views bảng lương
│   └── menu.xml
├── security/
│   └── ir.model.access.csv
└── README.md
```

## Hướng dẫn cài đặt

### 1. Cài đặt module
```bash
# Vào thư mục Odoo
cd odoo-fitdnu

# Cập nhật module
python3 odoo-bin -c odoo.conf -d database_name -u nhan_su

# Hoặc cài đặt mới
python3 odoo-bin -c odoo.conf -d database_name -i nhan_su
```

### 2. Khởi động lại Odoo (nếu cần)
```bash
python3 odoo-bin -c odoo.conf
```

## Hướng dẫn sử dụng

### Bước 1: Thiết lập danh mục
1. Vào menu **Quản Lý Nhân Sự → Danh mục → Phòng ban**
   - Tạo các phòng ban trong công ty
   - Thiết lập cấu trúc phòng ban cha - con nếu cần

2. Vào menu **Quản Lý Nhân Sự → Danh mục → Chức vụ**
   - Tạo các chức vụ
   - Thiết lập lương cơ bản và phụ cấp cho mỗi chức vụ

### Bước 2: Quản lý nhân viên
1. Vào menu **Quản Lý Nhân Sự → Nhân viên**
2. Tạo hồ sơ nhân viên với đầy đủ thông tin
3. Gán phòng ban và chức vụ cho nhân viên

### Bước 3: Chấm công
1. Vào menu **Quản Lý Nhân Sự → Chấm công → Chấm công hàng ngày**
2. Tạo bản ghi chấm công mỗi ngày:
   - Chọn nhân viên
   - Nhập giờ vào, giờ ra
   - Hệ thống tự động tính số giờ làm và phát hiện đi trễ/về sớm
3. Sử dụng chức năng check_in/check_out (có thể gọi từ code):
   ```python
   # Check-in
   self.env['cham_cong'].check_in(nhan_vien_id)
   
   # Check-out
   self.env['cham_cong'].check_out(nhan_vien_id)
   ```

### Bước 4: Báo cáo chấm công tháng
1. Vào menu **Quản Lý Nhân Sự → Chấm công → Báo cáo chấm công tháng**
2. Tạo báo cáo cho từng nhân viên theo tháng
3. Hệ thống sẽ tự động tổng hợp từ dữ liệu chấm công hàng ngày

### Bước 5: Tính lương
1. Vào menu **Quản Lý Nhân Sự → Bảng lương**
2. Tạo bảng lương mới:
   - Chọn nhân viên, tháng, năm
   - Hệ thống tự động điền lương cơ bản và phụ cấp từ chức vụ
   - Hệ thống tự động lấy thông tin công từ báo cáo chấm công
3. Điều chỉnh các khoản phụ cấp và khấu trừ nếu cần
4. Quy trình duyệt:
   - Nhấn **Gửi duyệt** khi đã nhập xong
   - Nhấn **Duyệt** để phê duyệt bảng lương
   - Nhấn **Đã chi trả** khi đã thanh toán cho nhân viên

## Công thức tính lương

### Lương thực tế theo ngày công
```
Lương theo ngày công = Lương cơ bản × (Số ngày công thực tế / 22)
Ngày công thực tế = Số ngày công - Nghỉ không phép
```

### Tiền tăng ca
```
Giá 1 giờ = Lương cơ bản / 176 giờ (22 ngày × 8 giờ)
Tiền tăng ca = Giá 1 giờ × Số giờ tăng ca × 1.5
```

### Tổng thu nhập
```
Tổng thu nhập = Lương theo ngày công + Phụ cấp chức vụ + Phụ cấp ăn trưa
              + Phụ cấp xăng xe + Phụ cấp điện thoại + Phụ cấp khác
              + Tiền tăng ca + Tiền thưởng
```

### Tổng khấu trừ
```
BHXH = Lương cơ bản × 8%
BHYT = Lương cơ bản × 1.5%
BHTN = Lương cơ bản × 1%

Tổng khấu trừ = BHXH + BHYT + BHTN + Thuế TNCN + Khấu trừ khác
```

### Thực lĩnh
```
Thực lĩnh = Tổng thu nhập - Tổng khấu trừ
```

## Chức năng nâng cao

### 1. Filter và Group by
- Lọc theo phòng ban, chức vụ, trạng thái
- Nhóm theo nhân viên, phòng ban, tháng, năm
- Tìm kiếm nhanh

### 2. Chatter và Activities
- Theo dõi lịch sử thay đổi bảng lương
- Tạo hoạt động nhắc nhở
- Thảo luận về bảng lương

### 3. Computed fields tự động
- Tự động tính tuổi từ ngày sinh
- Tự động tính số năm công tác
- Tự động tính số giờ làm việc
- Tự động tính tiền tăng ca
- Tự động tính các khoản khấu trừ bảo hiểm

### 4. Validation
- Giờ ra phải sau giờ vào
- Mã nhân viên, mã phòng ban, mã chức vụ phải duy nhất
- Không cho phép tạo trùng bảng lương cho cùng nhân viên trong cùng tháng

## Dependencies

- base
- mail (cho chatter và activities)

## Tác giả

FIT DNU - https://fit.dnu.edu.vn

## License

LGPL-3
