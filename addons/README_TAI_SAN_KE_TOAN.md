# HỆ THỐNG QUẢN LÝ TÀI SẢN VÀ KẾ TOÁN TÍCH HỢP

## 📋 MỤC LỤC

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Kiến trúc module](#2-kiến-trúc-module)
3. [Luồng hoạt động chi tiết](#3-luồng-hoạt-động-chi-tiết)
4. [Tích hợp giữa các module](#4-tích-hợp-giữa-các-module)
5. [Cơ chế khấu hao tự động](#5-cơ-chế-khấu-hao-tự-động)
6. [Hệ thống kế toán](#6-hệ-thống-kế-toán)
7. [Mô hình dữ liệu](#7-mô-hình-dữ-liệu)
8. [Use Cases thực tế](#8-use-cases-thực-tế)
9. [Hướng dẫn triển khai](#9-hướng-dẫn-triển-khai)

---

## 1. TỔNG QUAN HỆ THỐNG

### 1.1. Giới thiệu

Hệ thống gồm **3 module** tích hợp chặt chẽ với nhau:

```
┌─────────────────────────────────────────────────────────┐
│                    ODOO FITDNU                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   NHAN_SU    │◄─────│   TAI_SAN    │                │
│  │  (Nền tảng)  │      │(Quản lý TS)  │                │
│  └──────────────┘      └───────┬──────┘                │
│         ▲                      │                         │
│         │                      ▼                         │
│         │              ┌──────────────┐                 │
│         └──────────────│   KE_TOAN    │                 │
│                        │  (Kế toán)   │                 │
│                        └──────────────┘                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 1.2. Mục tiêu

- ✅ Quản lý tài sản cố định và khấu hao tự động
- ✅ Tích hợp sâu với hệ thống nhân sự
- ✅ Tự động ghi nhận bút toán kế toán
- ✅ Theo dõi chi phí theo phòng ban và nhân viên
- ✅ Tuân thủ chế độ kế toán Việt Nam

### 1.3. Công nghệ

- **Framework:** Odoo 15.0
- **Ngôn ngữ:** Python 3.10
- **Database:** PostgreSQL
- **Kiến trúc:** Model Inheritance & View Inheritance

---

## 2. KIẾN TRÚC MODULE

### 2.1. Module NHAN_SU (HR - Base Module)

**Vai trò:** Module nền tảng, cung cấp dữ liệu nhân viên và phòng ban

**Models:**
```python
nhan_vien       # Nhân viên
phong_ban       # Phòng ban
chuc_vu         # Chức vụ
cham_cong       # Chấm công
bang_luong      # Bảng lương
```

**Cấu trúc thư mục:**
```
nhan_su/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── nhan_vien.py       # Model nhân viên
│   ├── phong_ban.py       # Model phòng ban
│   └── ...
├── views/
│   ├── nhan_vien.xml      # Form view (có button_box)
│   ├── phong_ban.xml      # Form view (có button_box)
│   └── menu.xml
└── security/
    └── ir.model.access.csv
```

**Điểm quan trọng:**
- Form view có `<div name="button_box">` để các module khác extend
- Có `<notebook>` để thêm tabs mới
- Các field cơ bản: ma_dinh_danh, ho_ten, email, phong_ban_ids

---

### 2.2. Module TAI_SAN (Asset Management)

**Vai trò:** Quản lý tài sản và khấu hao, extend module NHAN_SU

**Models:**

```python
# Models chính
loai_tai_san    # Loại tài sản (máy móc, nhà, xe...)
tai_san         # Tài sản cụ thể
khau_hao        # Bản ghi khấu hao hàng tháng

# Model inheritance (extend nhan_su)
nhan_vien (inherit)  # Thêm fields: tai_san_quan_ly_ids, so_luong_tai_san_quan_ly
phong_ban (inherit)  # Thêm fields: tai_san_ids, tong_gia_tri_tai_san
```

**Cấu trúc thư mục:**
```
tai_san/
├── __init__.py
├── __manifest__.py
│   depends: ['base', 'nhan_su']
├── models/
│   ├── loai_tai_san.py         # Loại tài sản
│   ├── tai_san.py              # Tài sản
│   ├── khau_hao.py             # Khấu hao
│   └── nhan_su_inherit.py      # Extend HR models
├── views/
│   ├── loai_tai_san_view.xml
│   ├── tai_san_view.xml
│   ├── khau_hao_view.xml
│   ├── nhan_su_extend.xml      # Extend HR views
│   └── menu.xml                # Menu riêng + tích hợp
└── security/
    └── ir.model.access.csv
```

**Features:**
- ✅ 2 phương pháp khấu hao: Đường thẳng & Số dư giảm dần
- ✅ Tự động tính khấu hao hàng tháng
- ✅ Liên kết với nhân viên quản lý và phòng ban
- ✅ Button "Tạo khấu hao tháng này"
- ✅ Smart buttons trên form HR
- ✅ Tabs mới trong form HR

---

### 2.3. Module KE_TOAN (Accounting)

**Vai trò:** Hệ thống kế toán, tự động ghi nhận từ khấu hao

**Models:**

```python
# Models chính
tai_khoan_ke_toan   # Tài khoản kế toán (111, 112, 211, 214...)
so_cai              # Sổ cái (bút toán kế toán)

# Model inheritance (extend nhan_su & tai_san)
nhan_vien (inherit)  # Thêm: so_cai_lap_ids, so_cai_duyet_ids
phong_ban (inherit)  # Thêm: so_cai_ids, tong_gia_tri_chung_tu
khau_hao (inherit)   # Thêm: so_cai_id (liên kết với bút toán)
```

**Cấu trúc thư mục:**
```
ke_toan/
├── __init__.py
├── __manifest__.py
│   depends: ['base', 'nhan_su', 'tai_san']
├── models/
│   ├── tai_khoan_ke_toan.py    # Tài khoản kế toán
│   ├── so_cai.py               # Sổ cái
│   ├── nhan_su_inherit.py      # Extend HR models
│   └── khau_hao_inherit.py     # Extend khau_hao model
├── views/
│   ├── tai_khoan_ke_toan_view.xml
│   ├── so_cai_view.xml
│   ├── nhan_su_extend.xml      # Extend HR views
│   ├── khau_hao_extend.xml     # Extend khau_hao view
│   └── menu.xml
├── data/
│   └── tai_khoan_ke_toan_data.xml  # 22 tài khoản mặc định
└── security/
    └── ir.model.access.csv
```

**Features:**
- ✅ 22 tài khoản theo chế độ VN (8 cấp 2 + 14 cấp 3)
- ✅ Hệ thống phân cấp tài khoản (parent-child)
- ✅ Workflow: Nhập → Ghi sổ → Khóa sổ
- ✅ Tự động tạo bút toán từ khấu hao
- ✅ Tính toán Tổng Nợ, Tổng Có, Số dư

---

## 3. LUỒNG HOẠT ĐỘNG CHI TIẾT

### 3.1. Workflow tổng quan

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. KHỞI TẠO DỮ LIỆU (Module NHAN_SU)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Admin tạo:                                                      │
│  • Nhân viên: Nguyễn Văn A (Phòng IT)                          │
│  • Phòng ban: Phòng IT, Phòng Kế toán                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. QUẢN LÝ TÀI SẢN (Module TAI_SAN)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Bước 1: Tạo Loại tài sản                                       │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Mã: MAYTINH                                        │        │
│  │ Tên: Máy tính văn phòng                            │        │
│  │ Thời gian: 60 tháng                                │        │
│  │ Phương pháp: Đường thẳng                           │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  Bước 2: Tạo Tài sản                                            │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Mã: TS001                                          │        │
│  │ Tên: Dell Latitude 5420                            │        │
│  │ Loại: MAYTINH                                      │        │
│  │ Nguyên giá: 20,000,000 VNĐ                         │        │
│  │ Ngày mua: 01/01/2026                               │        │
│  │ Người quản lý: Nguyễn Văn A                        │        │
│  │ Phòng ban: Phòng IT                                │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  → Hệ thống tự động tính:                                       │
│    • Khấu hao/tháng = 20,000,000 / 60 = 333,333 VNĐ            │
│    • Giá trị còn lại = 20,000,000 VNĐ (ban đầu)                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. KHẤU HAO TỰ ĐỘNG (Module TAI_SAN)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User vào form tài sản TS001 → Click button:                   │
│  [Tạo khấu hao tháng này]                                       │
│                                                                  │
│  Hệ thống thực hiện:                                             │
│  ┌────────────────────────────────────────────────────┐        │
│  │ 1. Tạo bản ghi khau_hao:                          │        │
│  │    - tai_san_id: TS001                             │        │
│  │    - thang: 1                                      │        │
│  │    - nam: 2026                                     │        │
│  │    - gia_tri_khau_hao: 333,333                    │        │
│  │    - ngay_ghi_nhan: 31/01/2026                    │        │
│  │                                                     │        │
│  │ 2. Cập nhật tai_san:                               │        │
│  │    - gia_tri_khau_hao_luy_ke: 333,333            │        │
│  │    - gia_tri_con_lai: 19,666,667                  │        │
│  │    - so_thang_da_khau_hao: 1                      │        │
│  │                                                     │        │
│  │ 3. Nếu module KE_TOAN đã cài:                     │        │
│  │    → Gọi _tao_but_toan_ke_toan()                 │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. GHI NHẬN KẾ TOÁN (Module KE_TOAN)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Method _tao_but_toan_ke_toan() thực hiện:                      │
│                                                                  │
│  1. Kiểm tra module ke_toan đã cài:                             │
│     if 'so_cai' not in self.env: return                         │
│                                                                  │
│  2. Tìm tài khoản kế toán:                                      │
│     - TK 627: Chi phí khấu hao TSCĐ                            │
│     - TK 214: Hao mòn TSCĐ                                      │
│                                                                  │
│  3. Tạo bút toán kế toán:                                       │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Model: so_cai                                      │        │
│  │ ┌──────────────────────────────────────────┐      │        │
│  │ │ ma_chung_tu: KH-TS001-012026             │      │        │
│  │ │ ngay_ghi_so: 31/01/2026                  │      │        │
│  │ │ dien_giai: Khấu hao Dell Latitude...     │      │        │
│  │ │                                           │      │        │
│  │ │ tai_khoan_no_id: TK 627 (Chi phí)       │      │        │
│  │ │ tai_khoan_co_id: TK 214 (Hao mòn)       │      │        │
│  │ │ so_tien: 333,333                         │      │        │
│  │ │ loai_chung_tu: khau_hao                  │      │        │
│  │ │ trang_thai: nhap                         │      │        │
│  │ └──────────────────────────────────────────┘      │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  4. Liên kết ngược:                                              │
│     khau_hao.so_cai_id = so_cai.id                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. DUYỆT BÚT TOÁN (Module KE_TOAN)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Kế toán viên vào form sổ cái:                                 │
│                                                                  │
│  Trạng thái: [Nhập] → Click [Ghi sổ]                           │
│  • Tự động gán nguoi_duyet_id = user hiện tại                  │
│  • Chuyển trạng thái → [Đã ghi sổ]                             │
│  • Các field chính bị readonly                                  │
│                                                                  │
│  Trạng thái: [Đã ghi sổ] → Click [Khóa sổ]                     │
│  • Chuyển trạng thái → [Đã khóa sổ]                            │
│  • Không thể sửa gì nữa                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. CẬP NHẬT SỐ DƯ TÀI KHOẢN (Tự động)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Computed fields tự động tính:                                   │
│                                                                  │
│  TK 627 - Chi phí khấu hao TSCĐ:                               │
│  ┌────────────────────────────────────────────────────┐        │
│  │ tong_no = 333,333 (bút toán bên Nợ)              │        │
│  │ tong_co = 0                                        │        │
│  │ so_du = 333,333 (dư Nợ)                          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  TK 214 - Hao mòn TSCĐ:                                        │
│  ┌────────────────────────────────────────────────────┐        │
│  │ tong_no = 0                                        │        │
│  │ tong_co = 333,333 (bút toán bên Có)              │        │
│  │ so_du = 333,333 (dư Có)                          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. TÍCH HỢP GIỮA CÁC MODULE

### 4.1. TAI_SAN → NHAN_SU (Extend Models)

**File:** `tai_san/models/nhan_su_inherit.py`

```python
class NhanVienInherit(models.Model):
    _inherit = 'nhan_vien'
    
    # Thêm fields mới
    tai_san_quan_ly_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='nguoi_quan_ly_id',
        string='Tài sản quản lý'
    )
    
    so_luong_tai_san_quan_ly = fields.Integer(
        string="Số lượng tài sản",
        compute='_compute_so_luong_tai_san_quan_ly',
        store=True
    )
    
    @api.depends('tai_san_quan_ly_ids')
    def _compute_so_luong_tai_san_quan_ly(self):
        for record in self:
            record.so_luong_tai_san_quan_ly = len(record.tai_san_quan_ly_ids)
```

**Kết quả:**
- Model `nhan_vien` giờ có thêm 2 fields
- Không cần sửa code module `nhan_su`
- Khi uninstall `tai_san`, fields tự động biến mất

---

### 4.2. TAI_SAN → NHAN_SU (Extend Views)

**File:** `tai_san/views/nhan_su_extend.xml`

```xml
<record id="view_nhan_vien_form_tai_san" model="ir.ui.view">
    <field name="name">nhan_vien.form.tai_san</field>
    <field name="model">nhan_vien</field>
    <field name="inherit_id" ref="nhan_su.view_nhan_vien_form"/>
    <field name="arch" type="xml">
        
        <!-- Thêm Smart button -->
        <xpath expr="//div[@name='button_box']" position="inside">
            <button name="%(tai_san.action_tai_san)d" type="action" 
                    class="oe_stat_button" icon="fa-building"
                    context="{'search_default_nguoi_quan_ly_id': active_id}">
                <field name="so_luong_tai_san_quan_ly" widget="statinfo" string="Tài sản"/>
            </button>
        </xpath>
        
        <!-- Thêm Tab mới -->
        <xpath expr="//notebook" position="inside">
            <page string="Tài sản quản lý">
                <field name="tai_san_quan_ly_ids">
                    <tree>
                        <field name="ma_tai_san"/>
                        <field name="ten_tai_san"/>
                        <field name="loai_tai_san_id"/>
                        <field name="nguyen_gia"/>
                        <field name="gia_tri_con_lai"/>
                        <field name="trang_thai"/>
                    </tree>
                </field>
            </page>
        </xpath>
        
    </field>
</record>
```

**Kết quả:**
- Form nhân viên hiển thị smart button "Tài sản"
- Thêm tab "Tài sản quản lý"
- Click button → Filter tài sản của nhân viên đó

---

### 4.3. KE_TOAN → TAI_SAN (Extend Model khau_hao)

**File:** `ke_toan/models/khau_hao_inherit.py`

```python
class KhauHaoInherit(models.Model):
    _inherit = 'khau_hao'
    
    # Thêm field liên kết với sổ cái
    so_cai_id = fields.Many2one(
        comodel_name='so_cai',
        string="Sổ cái",
        ondelete='set null',
        help="Bút toán kế toán được tạo tự động"
    )
```

**Tại sao cần extend?**
- Module `tai_san` KHÔNG biết về model `so_cai`
- Nếu thêm trực tiếp → Lỗi khi `ke_toan` chưa cài
- Extend → Field chỉ xuất hiện khi `ke_toan` đã cài

---

### 4.4. Luồng gọi method giữa các module

```python
# File: tai_san/models/khau_hao.py

@api.model
def create(self, vals):
    record = super(KhauHao, self).create(vals)
    
    # Kiểm tra module ke_toan đã cài chưa
    if self.env['ir.module.module'].search([
        ('name', '=', 'ke_toan'), 
        ('state', '=', 'installed')
    ]):
        # Gọi method tạo bút toán
        record._tao_but_toan_ke_toan()
    
    return record

def _tao_but_toan_ke_toan(self):
    """Tạo bút toán kế toán cho khấu hao"""
    self.ensure_one()
    
    # Double check model tồn tại
    if 'so_cai' not in self.env:
        return
    
    # Tạo bút toán
    SoCai = self.env['so_cai']
    so_cai = SoCai.create({
        'ma_chung_tu': f'KH-{self.tai_san_id.ma_tai_san}-{self.thang:02d}{self.nam}',
        'ngay_ghi_so': self.ngay_ghi_nhan,
        'dien_giai': f'Khấu hao {self.tai_san_id.ten_tai_san} tháng {self.thang}/{self.nam}',
        'tai_khoan_no_id': tk_chi_phi_khau_hao.id,  # TK 627
        'tai_khoan_co_id': tk_khau_hao_luy_ke.id,   # TK 214
        'so_tien': self.gia_tri_khau_hao,
        'loai_chung_tu': 'khau_hao',
    })
    
    # Liên kết ngược (nếu field tồn tại)
    if hasattr(self, 'so_cai_id'):
        self.so_cai_id = so_cai.id
```

**Cơ chế:**
1. Check module đã cài: `search([('name', '=', 'ke_toan')])`
2. Check model tồn tại: `if 'so_cai' not in self.env`
3. Check field tồn tại: `if hasattr(self, 'so_cai_id')`
4. Không crash nếu module chưa cài

---

## 5. CƠ CHẾ KHẤU HAO TỰ ĐỘNG

### 5.1. Hai phương pháp khấu hao

#### **A. KHẤU HAO ĐƯỜNG THẲNG**

```python
@api.depends('loai_tai_san_id.thoi_gian_khau_hao', 'nguyen_gia', 'phuong_phap_khau_hao')
def _compute_khau_hao_hang_thang(self):
    for record in self:
        if record.phuong_phap_khau_hao == 'duong_thang':
            # Chia đều nguyên giá cho số tháng
            record.khau_hao_hang_thang = record.nguyen_gia / record.thoi_gian_khau_hao
```

**Ví dụ:**
```
Nguyên giá: 60,000,000 VNĐ
Thời gian: 60 tháng
→ Khấu hao/tháng = 60,000,000 / 60 = 1,000,000 VNĐ
```

#### **B. KHẤU HAO SỐ DƯ GIẢM DẦN**

```python
elif record.phuong_phap_khau_hao == 'so_du_giam_dan':
    # Tính theo giá trị còn lại
    ty_le_khau_hao_thang = (1.0 / record.thoi_gian_khau_hao) * record.loai_tai_san_id.he_so_khau_hao
    record.khau_hao_hang_thang = record.gia_tri_con_lai * ty_le_khau_hao_thang
```

**Ví dụ:**
```
Nguyên giá: 60,000,000 VNĐ
Thời gian: 60 tháng
Hệ số: 2.0

Tỷ lệ = (1/60) × 2.0 = 3.33%/tháng

Tháng 1: Khấu hao = 60,000,000 × 3.33% = 2,000,000
        Còn lại = 58,000,000
        
Tháng 2: Khấu hao = 58,000,000 × 3.33% = 1,933,333
        Còn lại = 56,066,667
```

---

### 5.2. Button "Tạo khấu hao tháng này"

```python
def action_tao_khau_hao_tu_dong(self):
    """Tạo khấu hao tự động cho tài sản"""
    self.ensure_one()
    
    # 1. Validate
    if self.trang_thai not in ['dang_su_dung', 'bao_tri']:
        raise ValidationError(_('Chỉ có thể tạo khấu hao cho tài sản đang sử dụng!'))
    
    # 2. Lấy tháng hiện tại
    ngay_hien_tai = date.today()
    thang_hien_tai = ngay_hien_tai.replace(day=1)
    
    # 3. Kiểm tra đã có khấu hao tháng này chưa
    khau_hao_da_co = self.env['khau_hao'].search([
        ('tai_san_id', '=', self.id),
        ('thang', '=', thang_hien_tai.month),
        ('nam', '=', thang_hien_tai.year)
    ])
    if khau_hao_da_co:
        raise ValidationError(_('Đã có khấu hao cho tháng này!'))
    
    # 4. Kiểm tra còn khấu hao không
    if self.so_thang_da_khau_hao >= self.thoi_gian_khau_hao:
        raise ValidationError(_('Tài sản đã khấu hao hết!'))
    
    # 5. Tạo bản ghi khấu hao
    self.env['khau_hao'].create({
        'tai_san_id': self.id,
        'thang': thang_hien_tai.month,
        'nam': thang_hien_tai.year,
        'gia_tri_khau_hao': self.khau_hao_hang_thang,
    })
    
    # 6. Cập nhật trạng thái nếu khấu hao hết
    if self.so_thang_da_khau_hao + 1 >= self.thoi_gian_khau_hao:
        self.trang_thai = 'khau_hao_het'
    
    # 7. Hiển thị thông báo
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Thành công'),
            'message': _('Đã tạo khấu hao'),
            'type': 'success',
        }
    }
```

---

## 6. HỆ THỐNG KẾ TOÁN

### 6.1. Cấu trúc tài khoản

**22 tài khoản theo chế độ Việt Nam:**

```
111 - Tiền mặt (Tài sản - Nợ)
  ├─ 1111 - Tiền Việt Nam
  └─ 1112 - Ngoại tệ

112 - Tiền gửi ngân hàng (Tài sản - Nợ)
  ├─ 1121 - Tiền VNĐ gửi ngân hàng
  └─ 1122 - Ngoại tệ gửi ngân hàng

211 - TSCĐ hữu hình (Tài sản - Nợ)
  ├─ 2111 - Nhà cửa, vật kiến trúc
  ├─ 2112 - Máy móc thiết bị
  ├─ 2113 - Phương tiện vận tải
  └─ 2114 - Thiết bị, dụng cụ quản lý

214 - Hao mòn TSCĐ (Tài sản điều chỉnh - Có)

411 - Nguồn vốn kinh doanh (Nguồn vốn - Có)

511 - Doanh thu (Doanh thu - Có)

627 - Chi phí khấu hao TSCĐ (Chi phí - Nợ)

642 - Chi phí QLDN (Chi phí - Nợ)
  ├─ 6421 - Chi phí nhân viên quản lý
  ├─ 6422 - Chi phí vật liệu quản lý
  ├─ 6423 - Chi phí đồ dùng văn phòng
  ├─ 6424 - Chi phí khấu hao TSCĐ QLDN
  ├─ 6425 - Chi phí dịch vụ mua ngoài
  └─ 6426 - Chi phí bằng tiền khác
```

---

### 6.2. Tính chất Nợ/Có

**Nguyên tắc:**

```python
@api.depends('tong_no', 'tong_co', 'tinh_chat')
def _compute_so_du(self):
    for record in self:
        if record.tinh_chat == 'no':
            # Tài khoản tài sản, chi phí → Số dư = Nợ - Có
            record.so_du = record.tong_no - record.tong_co
        elif record.tinh_chat == 'co':
            # Tài khoản nguồn vốn, doanh thu → Số dư = Có - Nợ
            record.so_du = record.tong_co - record.tong_no
```

**Ví dụ:**

| TK | Loại | Tính chất | Tăng ở | Giảm ở | Số dư |
|----|------|-----------|--------|--------|-------|
| 111 | Tài sản | Nợ | Nợ | Có | Nợ |
| 214 | Điều chỉnh | Có | Có | Nợ | Có |
| 411 | Nguồn vốn | Có | Có | Nợ | Có |
| 511 | Doanh thu | Có | Có | Nợ | Có |
| 627 | Chi phí | Nợ | Nợ | Có | Nợ |

---

### 6.3. Workflow bút toán

```
┌─────────────────────────────────────────────┐
│        TRẠNG THÁI SỔ CÁI                    │
├─────────────────────────────────────────────┤
│                                              │
│  [NHẬP] (nhap)                              │
│   • Vừa tạo (từ khấu hao hoặc thủ công)    │
│   • Có thể sửa tất cả fields               │
│   • Button: [Ghi sổ]                        │
│                                              │
│          ▼ Click [Ghi sổ]                   │
│                                              │
│  [ĐÃ GHI SỔ] (da_ghi_so)                   │
│   • Tự động gán nguoi_duyet_id             │
│   • Readonly: TK, số tiền, loại            │
│   • Có thể sửa: Ghi chú                     │
│   • Button: [Khóa sổ]                       │
│                                              │
│          ▼ Click [Khóa sổ]                  │
│                                              │
│  [ĐÃ KHÓA SỔ] (da_khoa_so)                 │
│   • Readonly: Tất cả                        │
│   • Không có button nào                     │
│   • Không thể xóa                           │
│                                              │
└─────────────────────────────────────────────┘
```

**Code:**

```python
def action_ghi_so(self):
    """Ghi sổ chứng từ"""
    for record in self:
        if record.trang_thai == 'nhap':
            if not record.nguoi_duyet_id and self.env.user.employee_id:
                record.nguoi_duyet_id = self.env.user.employee_id
            record.trang_thai = 'da_ghi_so'
    
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Thành công'),
            'message': _('Đã ghi sổ chứng từ'),
            'type': 'success',
        }
    }

def action_khoa_so(self):
    """Khóa sổ chứng từ"""
    for record in self:
        if record.trang_thai == 'da_ghi_so':
            record.trang_thai = 'da_khoa_so'
    
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Thành công'),
            'message': _('Đã khóa sổ chứng từ'),
            'type': 'success',
        }
    }
```

---

## 7. MÔ HÌNH DỮ LIỆU

### 7.1. ERD (Entity Relationship Diagram)

```
┌─────────────────┐          ┌─────────────────┐
│   NHAN_VIEN     │◄─────────│    TAI_SAN      │
│                 │ 1      * │                 │
│ - ma_dinh_danh  │          │ - ma_tai_san    │
│ - ho_ten        │          │ - ten_tai_san   │
│ - email         │          │ - nguyen_gia    │
│                 │          │ - gia_tri_con_lai│
└────────┬────────┘          └────────┬────────┘
         │                            │
         │ *                          │ 1
         │                            │
         │                   ┌────────▼────────┐
         │                   │  LOAI_TAI_SAN   │
         │                   │                 │
         │                   │ - ma_loai       │
         │                   │ - ten_loai      │
         │                   │ - thoi_gian_kh  │
         │                   └─────────────────┘
         │
         │
┌────────▼────────┐          ┌─────────────────┐
│   PHONG_BAN     │◄─────────│    TAI_SAN      │
│                 │ 1      * │                 │
│ - ma_dinh_danh  │          │ - phong_ban_id  │
│ - ten_phong_ban │          │                 │
└─────────────────┘          └────────┬────────┘
                                      │ 1
                                      │
                                      │ *
                             ┌────────▼────────┐
                             │    KHAU_HAO     │
                             │                 │
                             │ - thang         │
                             │ - nam           │
                             │ - gia_tri_kh    │
                             └────────┬────────┘
                                      │ 1
                                      │
                                      │ 1
                             ┌────────▼────────┐
                             │     SO_CAI      │
                             │                 │
                             │ - ma_chung_tu   │
                             │ - ngay_ghi_so   │
                             │ - so_tien       │
                             └────────┬────────┘
                                      │ *
                        ┌─────────────┴─────────────┐
                        │                           │
                        │ 1                         │ 1
               ┌────────▼────────┐        ┌────────▼────────┐
               │ TAI_KHOAN_KE_   │        │ TAI_KHOAN_KE_   │
               │ TOAN (Nợ)       │        │ TOAN (Có)       │
               │                 │        │                 │
               │ - ma_tai_khoan  │        │ - ma_tai_khoan  │
               │ - ten_tai_khoan │        │ - ten_tai_khoan │
               └─────────────────┘        └─────────────────┘
```

---

### 7.2. Dependencies giữa các module

```
graph TD
    BASE[Base Module - Odoo Core]
    NHAN_SU[Module NHAN_SU]
    TAI_SAN[Module TAI_SAN]
    KE_TOAN[Module KE_TOAN]
    
    BASE --> NHAN_SU
    BASE --> TAI_SAN
    NHAN_SU --> TAI_SAN
    NHAN_SU --> KE_TOAN
    TAI_SAN --> KE_TOAN
    
    style BASE fill:#e1f5ff
    style NHAN_SU fill:#fff9c4
    style TAI_SAN fill:#c8e6c9
    style KE_TOAN fill:#f8bbd0
```

**Manifest dependencies:**

```python
# nhan_su/__manifest__.py
'depends': ['base']

# tai_san/__manifest__.py
'depends': ['base', 'nhan_su']

# ke_toan/__manifest__.py
'depends': ['base', 'nhan_su', 'tai_san']
```

---

## 8. USE CASES THỰC TẾ

### Use Case 1: Mua máy tính mới

**Actors:** Admin, Kế toán viên

**Scenario:**

1. **Admin tạo tài sản:**
   - Menu: QLNS → Tài sản → Danh sách tài sản → Create
   - Mã: TS002
   - Tên: MacBook Pro M3
   - Loại: Máy tính (60 tháng, Số dư giảm dần, hệ số 2.0)
   - Nguyên giá: 50,000,000 VNĐ
   - Người quản lý: Nguyễn Văn B
   - Phòng ban: Phòng Marketing

2. **Hệ thống tự động:**
   - Tính khấu hao tháng đầu = 50,000,000 × (2/60) = 1,666,667 VNĐ
   - Hiển thị trên form nhân viên Nguyễn Văn B
   - Cập nhật số lượng tài sản Phòng Marketing

3. **Cuối tháng, Admin tạo khấu hao:**
   - Vào form TS002 → Click "Tạo khấu hao tháng này"
   - Hệ thống tạo bản ghi khau_hao
   - Tự động tạo bút toán kế toán

4. **Kế toán viên duyệt:**
   - Menu: QLNS → Kế toán → Sổ cái
   - Filter: Loại = Khấu hao, Trạng thái = Nhập
   - Click vào bút toán → [Ghi sổ] → [Khóa sổ]

5. **Xem báo cáo:**
   - TK 627: Tổng Nợ tăng 1,666,667
   - TK 214: Tổng Có tăng 1,666,667
   - Form Nguyễn Văn B: Smart button "Tài sản" hiển thị 1
   - Form Phòng Marketing: Tổng giá trị tài sản = 48,333,333

---

### Use Case 2: Xem báo cáo tài sản theo nhân viên

**Actors:** Quản lý

**Scenario:**

1. **Vào danh sách nhân viên:**
   - Menu: QLNS → Nhân viên
   - Click vào "Nguyễn Văn A"

2. **Xem thông tin tài sản:**
   - Smart button "Tài sản": 3 ← Số lượng
   - Click button → Mở danh sách tài sản (đã filter)
   - Tab "Tài sản quản lý": Tree view 3 tài sản

3. **Xem thông tin kế toán:**
   - Smart button "CT Đã lập": 25 ← Số chứng từ
   - Tab "Chứng từ kế toán":
     - Group "Đã lập": 25 bản ghi
     - Group "Đã duyệt": 10 bản ghi

---

### Use Case 3: Báo cáo tài sản theo phòng ban

**Actors:** Quản lý, Kế toán

**Scenario:**

1. **Vào danh sách phòng ban:**
   - Menu: QLNS → Phòng ban
   - Click vào "Phòng IT"

2. **Xem tổng quan:**
   - Smart button "Tài sản": 15
   - Field "Tổng giá trị tài sản": 500,000,000 VNĐ
   - Smart button "Chứng từ": 180
   - Field "Tổng giá trị chứng từ": 250,000,000 VNĐ

3. **Xem chi tiết:**
   - Tab "Tài sản": Tree view 15 tài sản
   - Tab "Chứng từ kế toán": Tree view 180 bút toán
   - Filter, group theo loại tài sản, trạng thái

---

## 9. HƯỚNG DẪN TRIỂN KHAI

### 9.1. Yêu cầu hệ thống

```
- Odoo: 15.0
- Python: 3.10+
- PostgreSQL: 12+
- OS: Ubuntu 22.04 (WSL hoặc native)
```

---

### 9.2. Cài đặt từng bước

#### **Bước 1: Chuẩn bị**

```bash
cd /home/an/odoo-fitdnu
```

Kiểm tra 3 module tồn tại:
```bash
ls -la addons/ | grep -E "nhan_su|tai_san|ke_toan"
```

---

#### **Bước 2: Cài đặt theo thứ tự**

**Quan trọng: PHẢI cài đúng thứ tự!**

```bash
# 1. Upgrade NHAN_SU (thêm button_box)
python3 odoo-bin -c odoo.conf -d your_database -u nhan_su --stop-after-init

# 2. Install TAI_SAN
python3 odoo-bin -c odoo.conf -d your_database -i tai_san --stop-after-init

# 3. Install KE_TOAN
python3 odoo-bin -c odoo.conf -d your_database -i ke_toan --stop-after-init
```

Hoặc cài tất cả cùng lúc:
```bash
python3 odoo-bin -c odoo.conf -d your_database -u nhan_su -i tai_san,ke_toan --stop-after-init
```

---

#### **Bước 3: Khởi động server**

```bash
python3 odoo-bin -c odoo.conf
```

Truy cập: http://localhost:8069

---

#### **Bước 4: Kiểm tra cài đặt**

1. **Menu QLNS:**
   - Có submenu "Tài sản" (3 items)
   - Có submenu "Kế toán" (2 items)

2. **Form Nhân viên:**
   - Có `<div name="button_box">` rỗng
   - Có smart button "Tài sản"
   - Có smart button "CT Đã lập"
   - Có tab "Tài sản quản lý"
   - Có tab "Chứng từ kế toán"

3. **Form Phòng ban:**
   - Có smart buttons
   - Có tabs mới
   - Có fields computed

4. **Tài khoản kế toán:**
   - Menu: QLNS → Kế toán → Tài khoản kế toán
   - Có 22 tài khoản (111, 1111, 1112, 112, ...)

---

### 9.3. Dữ liệu test

#### **A. Tạo Nhân viên:**

```
Mã: NV001
Tên: Nguyễn Văn A
Email: a.nguyen@company.com
Phòng ban: Phòng IT
```

#### **B. Tạo Loại tài sản:**

```
Mã: MAYTINH
Tên: Máy tính văn phòng
Thời gian: 60 tháng
Phương pháp: Đường thẳng
```

```
Mã: XEOTO
Tên: Xe ô tô
Thời gian: 96 tháng (8 năm)
Phương pháp: Số dư giảm dần
Hệ số: 2.0
```

#### **C. Tạo Tài sản:**

```
Mã: TS001
Tên: Dell Latitude 5420
Loại: MAYTINH
Nguyên giá: 20,000,000
Ngày mua: 01/01/2026
Người quản lý: Nguyễn Văn A
Phòng ban: Phòng IT
```

#### **D. Tạo khấu hao:**

- Vào form TS001
- Click "Tạo khấu hao tháng này"
- Kiểm tra bản ghi khau_hao
- Kiểm tra bút toán so_cai tự động

#### **E. Duyệt bút toán:**

- Menu: QLNS → Kế toán → Sổ cái
- Click vào bút toán
- [Ghi sổ] → [Khóa sổ]

---

### 9.4. Troubleshooting

#### **Lỗi: View inheritance không có button_box**

```
Lỗi: '<xpath expr="//div[@name='button_box']">' không thể nằm trong giao diện cha
```

**Nguyên nhân:** View nhan_vien chưa có button_box

**Giải pháp:**
```bash
# Kiểm tra file
cat addons/nhan_su/views/nhan_vien.xml | grep button_box

# Phải có:
<div class="oe_button_box" name="button_box">
</div>
```

---

#### **Lỗi: Model so_cai không tồn tại**

```
AttributeError: '_unknown' object has no attribute 'id'
```

**Nguyên nhân:** Module tai_san có field so_cai_id nhưng ke_toan chưa cài

**Giải pháp:** Đã fix bằng cách:
- Xóa field `so_cai_id` khỏi `tai_san/models/khau_hao.py`
- Thêm field qua extend: `ke_toan/models/khau_hao_inherit.py`

---

#### **Lỗi: Xpath không tìm thấy element**

```
ParseError: Xpath not found: //notebook/page[@string='Bảng lương']
```

**Nguyên nhân:** Không được dùng `@string` làm selector

**Giải pháp:**
```xml
<!-- SAI -->
<xpath expr="//notebook/page[@string='Bảng lương']" position="after">

<!-- ĐÚNG -->
<xpath expr="//notebook" position="inside">
```

---

### 9.5. Uninstall

**Thứ tự uninstall (ngược lại):**

```bash
# 1. Uninstall KE_TOAN trước
python3 odoo-bin -c odoo.conf -d your_database -u ke_toan --stop-after-init

# 2. Uninstall TAI_SAN
python3 odoo-bin -c odoo.conf -d your_database -u tai_san --stop-after-init

# 3. NHAN_SU giữ lại (hoặc uninstall nếu cần)
```

---

## 10. KẾT LUẬN

### 10.1. Ưu điểm hệ thống

✅ **Tích hợp chặt chẽ:** 3 module hoạt động như 1 hệ thống duy nhất  
✅ **Tự động hóa:** Khấu hao → Bút toán kế toán hoàn toàn tự động  
✅ **Mở rộng tốt:** Dùng inheritance, không sửa code gốc  
✅ **Dễ bảo trì:** Mỗi module độc lập, có thể uninstall riêng  
✅ **Tuân thủ chuẩn:** Theo chế độ kế toán Việt Nam  
✅ **User-friendly:** Smart buttons, tabs, computed fields real-time  

### 10.2. Hạn chế & Cải tiến

**Hạn chế:**
- Chưa có báo cáo in (reports)
- Chưa có dashboard/charts
- Chưa có API REST
- Chưa có import/export Excel

**Roadmap cải tiến:**
- [ ] Báo cáo PDF khấu hao
- [ ] Dashboard tài sản theo phòng ban
- [ ] Cảnh báo tài sản cần bảo trì
- [ ] Lịch khấu hao tự động (scheduled action)
- [ ] Module Bảo trì tài sản
- [ ] Tích hợp với module Mua hàng

---

## 11. LIÊN HỆ & HỖ TRỢ

**Developer:** Your Company  
**Version:** 15.0.1.0.0  
**Last Updated:** 06/01/2026  

**Tài liệu tham khảo:**
- Odoo Documentation: https://www.odoo.com/documentation/15.0/
- Chế độ kế toán Việt Nam: Thông tư 200/2014/TT-BTC

---

**END OF DOCUMENT**
