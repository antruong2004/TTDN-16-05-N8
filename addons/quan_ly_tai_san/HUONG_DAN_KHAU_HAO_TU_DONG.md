# TÍNH NĂNG TỰ ĐỘNG KHẤU HAO TÀI SẢN

## Mô tả
Tính năng tự động tính khấu hao tài sản theo định kỳ hàng tháng, tự động tạo bút toán kế toán và ghi nhận vào sổ cái.

## Tính năng chính

### 1. Tính khấu hao tự động
- ⏰ Chạy tự động vào **ngày 28 hàng tháng lúc 23:00**
- 📊 Hỗ trợ 3 phương pháp khấu hao:
  - **Đường thẳng**: Khấu hao đều theo tháng
  - **Số dư giảm dần**: Khấu hao cao ở đầu kỳ, giảm dần về cuối
  - **Tổng số năm**: Khấu hao theo tỷ lệ thời gian còn lại

### 2. Tự động tạo bút toán kế toán
- 🧾 Tự động tạo bút toán: **Nợ TK 6274** (Chi phí khấu hao) / **Có TK 2141** (Hao mòn TSCĐ)
- 📝 Liên kết với kỳ kế toán tương ứng
- ✅ Trạng thái bút toán: **Đã ghi sổ**

### 3. Thông báo tài sản sắp hết khấu hao
- 🔔 Gửi thông báo khi tài sản đã khấu hao **≥ 90%** giá trị
- 📅 Chạy vào **ngày 1 hàng tháng lúc 08:00**

## Cách sử dụng

### Bước 1: Cài đặt/Nâng cấp Module
```bash
# Upgrade module quan_ly_tai_san
python3 odoo-bin -c odoo.conf -u quan_ly_tai_san -d odoo_fresh
```

### Bước 2: Kiểm tra Scheduled Actions
1. Vào **Settings → Technical → Automation → Scheduled Actions**
2. Tìm các action:
   - **Tính khấu hao tài sản tự động**
   - **Thông báo tài sản sắp khấu hao xong**
3. Đảm bảo trạng thái **Active = True**

### Bước 3: Thiết lập Tài sản
Để tài sản được khấu hao tự động, cần:
- ✅ **Trạng thái**: Đang sử dụng
- ✅ **Giá trị ban đầu** > 0
- ✅ **Thời gian sử dụng** > 0
- ✅ **Ngày bắt đầu sử dụng** ≤ Ngày hiện tại
- ✅ **Phương pháp khấu hao**: Chọn 1 trong 3 phương pháp

### Bước 4: Chạy thủ công (Test)
Nếu muốn test ngay không cần đợi:
1. Vào **Settings → Technical → Automation → Scheduled Actions**
2. Chọn **Tính khấu hao tài sản tự động**
3. Click nút **Run Manually**

Hoặc dùng Python code trong console:
```python
# Tính khấu hao cho tất cả tài sản
self.env['khau_hao'].tao_khau_hao_tu_dong()

# Tính khấu hao cho 1 tài sản cụ thể
tai_san = self.env['tai_san'].browse(tai_san_id)
gia_tri = self.env['khau_hao'].tinh_gia_tri_khau_hao_thang(tai_san)
```

## Công thức tính khấu hao

### 1. Phương pháp Đường thẳng
```
Khấu hao tháng = Giá trị ban đầu / Số tháng sử dụng
```

**Ví dụ:**
- Giá trị ban đầu: 100,000,000 VNĐ
- Thời gian sử dụng: 60 tháng (5 năm)
- Khấu hao/tháng: 100,000,000 / 60 = **1,666,667 VNĐ**

### 2. Phương pháp Số dư giảm dần
```
Khấu hao tháng = Giá trị còn lại × (Tỷ lệ khấu hao % / 12)
```

**Ví dụ:**
- Giá trị ban đầu: 100,000,000 VNĐ
- Tỷ lệ khấu hao: 20%/năm
- Tháng 1: 100,000,000 × (20% / 12) = **1,666,667 VNĐ**
- Tháng 2: 98,333,333 × (20% / 12) = **1,638,889 VNĐ**
- ...giảm dần theo tháng

### 3. Phương pháp Tổng số năm
```
Khấu hao tháng = (Số tháng còn lại / Tổng số tháng) × Giá trị ban đầu
```

**Ví dụ:**
- Giá trị ban đầu: 100,000,000 VNĐ
- Thời gian sử dụng: 60 tháng
- Tổng số: 1+2+...+60 = 1,830
- Tháng 1: (60/1830) × 100,000,000 = **3,278,689 VNĐ**

## Xem Log và Theo dõi

### Xem Log trong Odoo
```bash
# Xem log file
tail -f /home/an/odoo-fitdnu/odoo.log | grep "KHẤU HAO"
```

Các log quan trọng:
- `====== BẮT ĐẦU TÍNH KHẤU HAO TỰ ĐỘNG ======`
- `Tìm thấy X tài sản cần khấu hao`
- `Tạo khấu hao cho TS001: 1,666,667 VNĐ`
- `====== HOÀN THÀNH: Đã tạo X bút toán khấu hao ======`

### Kiểm tra kết quả
1. **Menu Tài Sản → Khấu Hao**: Xem danh sách bút toán khấu hao
2. **Menu Kế Toán → Bút Toán**: Xem bút toán kế toán đã tạo
3. **Menu Tài Sản → Tài Sản**: Xem giá trị còn lại của từng tài sản

## Cấu hình nâng cao

### Thay đổi thời gian chạy Cron
Chỉnh sửa file `data/cron_khau_hao.xml`:

```xml
<!-- Chạy vào ngày 25 hàng tháng lúc 22:00 -->
<field name="nextcall" eval="(DateTime.now() + relativedelta(day=25, hour=22, minute=0, second=0)).strftime('%Y-%m-%d %H:%M:%S')"/>
```

### Vô hiệu hóa tự động khấu hao
1. Vào **Settings → Technical → Automation → Scheduled Actions**
2. Tìm **Tính khấu hao tài sản tự động**
3. Bỏ tick **Active**

### Thay đổi tài khoản kế toán
Chỉnh sửa hàm `_tao_but_toan_ke_toan()` trong file `models/khau_hao.py`:

```python
# Thay đổi TK chi phí (mặc định: 6274)
tk_chi_phi = self.env['ke_toan.tai_khoan'].search([
    ('ma_tai_khoan', '=', '6421')  # Đổi thành TK khác
], limit=1)

# Thay đổi TK hao mòn (mặc định: 2141)
tk_hao_mon = self.env['ke_toan.tai_khoan'].search([
    ('ma_tai_khoan', '=', '2143')  # Đổi thành TK khác
], limit=1)
```

## Xử lý lỗi

### Lỗi: "Không tìm thấy tài khoản kế toán"
**Nguyên nhân:** Chưa có TK 6274 hoặc TK 2141 trong hệ thống

**Giải pháp:** Đảm bảo đã tạo các tài khoản này trong module kế toán

### Lỗi: "Không tìm thấy kỳ kế toán"
**Nguyên nhân:** Chưa có kỳ kế toán cho tháng hiện tại

**Giải pháp:** Tạo kỳ kế toán trước khi chạy khấu hao

### Tài sản không được khấu hao
**Kiểm tra:**
1. Trạng thái tài sản = "Đang sử dụng"?
2. Giá trị ban đầu > 0?
3. Thời gian sử dụng > 0?
4. Đã khấu hao đủ 100% chưa?
5. Đã có khấu hao cho tháng này chưa?

## API Reference

### `tinh_gia_tri_khau_hao_thang(tai_san)`
Tính giá trị khấu hao cho 1 tài sản trong tháng

**Tham số:**
- `tai_san`: record của model `tai_san`

**Trả về:** `float` - Giá trị khấu hao (VNĐ)

### `tao_khau_hao_tu_dong()`
Tạo khấu hao tự động cho tất cả tài sản đủ điều kiện

**Trả về:** `dict`
```python
{
    'so_khau_hao': 10,  # Số bút toán đã tạo
    'tong_gia_tri': 15000000.0  # Tổng giá trị khấu hao
}
```

### `action_tinh_lai_khau_hao()`
Tính lại giá trị khấu hao cho các bút toán nháp

## Báo cáo và Thống kê

Sau khi có dữ liệu khấu hao, bạn có thể:
- Xem **Dashboard Tài Sản** để theo dõi tổng khấu hao
- Xem **Báo cáo Sổ Cái** để kiểm tra chi tiết bút toán
- Xem **Lịch sử Khấu hao** của từng tài sản

## Lưu ý quan trọng

⚠️ **Không sửa hoặc xóa** bút toán khấu hao đã ghi sổ  
⚠️ **Backup database** trước khi chạy khấu hao lần đầu  
⚠️ **Kiểm tra cẩn thận** cấu hình tài khoản kế toán  
⚠️ **Test thủ công** trước khi để cron tự động chạy  

## Hỗ trợ

Nếu có vấn đề, liên hệ:
- Email: fit@dnu.edu.vn
- Xem log tại: `/home/an/odoo-fitdnu/odoo.log`
