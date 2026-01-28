# -*- coding: utf-8 -*-
<<<<<<< HEAD

from odoo import models, fields, api
from calendar import monthrange
=======
from odoo import models, fields, api, exceptions
from datetime import datetime
>>>>>>> cc63fe88 (update)


class BangLuong(models.Model):
    _name = 'bang_luong'
<<<<<<< HEAD
    _description = 'Bảng lương'
    _order = 'nam desc, thang desc'

    # ================= BASIC =================

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    thang = fields.Selection(
        selection=[
            ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
            ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
            ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
            ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
        ],
        string="Tháng",
        required=True
    )

    nam = fields.Char(
        string="Năm",
        required=True
    )

    # ================= RELATED INFO =================

    chuc_vu_id = fields.Many2one(
        comodel_name='chuc_vu',
        string="Chức vụ",
        related='nhan_vien_id.chuc_vu_id',
        store=True
    )

    # 🔥 LƯƠNG LẤY TỪ NHÂN VIÊN (KHÔNG LẤY TỪ CHỨC VỤ)
    luong_co_ban = fields.Float(
        string="Lương cơ bản",
        compute="_compute_luong_co_ban",
        store=True
    )

    @api.depends('nhan_vien_id', 'nhan_vien_id.luong')
    def _compute_luong_co_ban(self):
        for record in self:
            record.luong_co_ban = record.nhan_vien_id.luong if record.nhan_vien_id else 0

    # ================= CHẤM CÔNG =================

    so_ngay_lam_viec = fields.Integer(
        string="Số ngày làm việc",
        compute='_compute_so_ngay_lam_viec',
        store=True
    )

    so_gio_lam_viec = fields.Float(
        string="Số giờ làm việc",
        compute='_compute_so_gio_lam_viec',
        store=True
    )

    so_ngay_nghi_phep = fields.Integer(
        string="Số ngày nghỉ phép",
        compute='_compute_so_ngay_nghi_phep',
        store=True
    )

    so_ngay_nghi_khong_phep = fields.Integer(
        string="Số ngày nghỉ không phép",
        compute='_compute_so_ngay_nghi_khong_phep',
        store=True
    )

    # ================= PHỤ CẤP =================

    so_gio_chuan = fields.Float(
        string="Số giờ chuẩn",
        default=192.0,  # 24 công x 8 giờ
        help="Số giờ làm việc chuẩn trong tháng (24 công x 8 giờ = 192 giờ)"
    )

    luong_theo_gio = fields.Float(
        string="Lương theo giờ",
        compute='_compute_luong_theo_gio',
        store=True,
        help="Lương cơ bản / Số giờ chuẩn"
    )

    luong_thuc_nhan = fields.Float(
        string="Lương theo giờ làm",
        compute='_compute_luong_thuc_nhan',
        store=True,
        help="Số giờ làm thực tế x Lương theo giờ"
    )

    phu_cap = fields.Float(string="Phụ cấp", default=0.0)
    thuong = fields.Float(string="Thưởng", default=0.0)
    tru_di = fields.Float(string="Khấu trừ", default=0.0)

    luong_lam_them = fields.Float(
        string="Lương làm thêm",
        compute='_compute_luong_lam_them',
        store=True
    )

    tong_luong = fields.Float(
        string="Tổng lương",
        compute='_compute_tong_luong',
        store=True
    )

    ghi_chu = fields.Text(string="Ghi chú")

    # ================= RELATIONS =================
    
    chi_tiet_cham_cong_ids = fields.One2many(
        comodel_name='cham_cong',
        string='Chi tiết chấm công',
        compute='_compute_chi_tiet_cham_cong',
        store=False
    )

    # ================= STATE =================

    trang_thai = fields.Selection(
        selection=[
            ('chua_duyet', 'Chưa duyệt'),
            ('da_duyet', 'Đã duyệt'),
            ('da_thanh_toan', 'Đã thanh toán'),
        ],
        string="Trạng thái",
        default='chua_duyet',
        required=True
    )

    # ================= COMPUTE FUNCTIONS =================

    def _get_date_range(self, record):
        """Lấy khoảng thời gian đầu và cuối tháng"""
        if not record.nam or not record.thang:
            return None, None
        try:
            last_day = monthrange(int(record.nam), int(record.thang))[1]
            return (
                f"{record.nam}-{record.thang.zfill(2)}-01",
                f"{record.nam}-{record.thang.zfill(2)}-{last_day}"
            )
        except (ValueError, calendar.IllegalMonthError):
            return None, None

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_so_ngay_lam_viec(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start, end = self._get_date_range(record)
                if start and end:
                    record.so_ngay_lam_viec = self.env['cham_cong'].search_count([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_lam', '>=', start),
                        ('ngay_lam', '<=', end),
                        ('loai_cham_cong', '=', 'di_lam')
                    ])
                else:
                    record.so_ngay_lam_viec = 0
            else:
                record.so_ngay_lam_viec = 0

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_so_gio_lam_viec(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start, end = self._get_date_range(record)
                if start and end:
                    cham_cong = self.env['cham_cong'].search([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_lam', '>=', start),
                        ('ngay_lam', '<=', end),
                        ('loai_cham_cong', '=', 'di_lam')
                    ])
                    record.so_gio_lam_viec = sum(cham_cong.mapped('so_gio_lam'))
                else:
                    record.so_gio_lam_viec = 0
            else:
                record.so_gio_lam_viec = 0

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_so_ngay_nghi_phep(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start, end = self._get_date_range(record)
                if start and end:
                    record.so_ngay_nghi_phep = self.env['cham_cong'].search_count([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_lam', '>=', start),
                        ('ngay_lam', '<=', end),
                        ('loai_cham_cong', '=', 'nghi_phep')
                    ])
                else:
                    record.so_ngay_nghi_phep = 0
            else:
                record.so_ngay_nghi_phep = 0

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_so_ngay_nghi_khong_phep(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start, end = self._get_date_range(record)
                if start and end:
                    record.so_ngay_nghi_khong_phep = self.env['cham_cong'].search_count([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_lam', '>=', start),
                        ('ngay_lam', '<=', end),
                        ('loai_cham_cong', '=', 'nghi_khong_phep')
                    ])
                else:
                    record.so_ngay_nghi_khong_phep = 0
            else:
                record.so_ngay_nghi_khong_phep = 0

    @api.depends('nhan_vien_id', 'thang', 'nam', 'luong_theo_gio')
    def _compute_luong_lam_them(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start, end = self._get_date_range(record)
                if start and end:
                    cham_cong = self.env['cham_cong'].search([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_lam', '>=', start),
                        ('ngay_lam', '<=', end),
                        ('loai_cham_cong', '=', 'lam_them')
                    ])
                    so_gio = sum(cham_cong.mapped('so_gio_lam'))
                    record.luong_lam_them = so_gio * record.luong_theo_gio * 1.5
                else:
                    record.luong_lam_them = 0
            else:
                record.luong_lam_them = 0

    @api.depends('luong_co_ban', 'so_gio_chuan')
    def _compute_luong_theo_gio(self):
        """Tính lương theo giờ = Lương cơ bản / Số giờ chuẩn"""
        for record in self:
            if record.luong_co_ban and record.so_gio_chuan:
                record.luong_theo_gio = record.luong_co_ban / record.so_gio_chuan
            else:
                record.luong_theo_gio = 0

    @api.depends('so_gio_lam_viec', 'luong_theo_gio')
    def _compute_luong_thuc_nhan(self):
        """Tính lương thực nhận = Số giờ làm x Lương theo giờ"""
        for record in self:
            record.luong_thuc_nhan = record.so_gio_lam_viec * record.luong_theo_gio

    @api.depends('luong_thuc_nhan', 'phu_cap', 'thuong', 'tru_di', 'luong_lam_them')
    def _compute_tong_luong(self):
        """Tổng lương = Lương theo giờ làm + Phụ cấp + Thưởng + Lương làm thêm - Khấu trừ"""
        for record in self:
            record.tong_luong = record.luong_thuc_nhan + record.phu_cap + record.thuong + record.luong_lam_them - record.tru_di

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_chi_tiet_cham_cong(self):
        """Lấy danh sách chấm công chi tiết trong tháng"""
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start, end = self._get_date_range(record)
                if start and end:
                    cham_cong_ids = self.env['cham_cong'].search([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_lam', '>=', start),
                        ('ngay_lam', '<=', end)
                    ], order='ngay_lam asc')
                    record.chi_tiet_cham_cong_ids = cham_cong_ids
                else:
                    record.chi_tiet_cham_cong_ids = False
            else:
                record.chi_tiet_cham_cong_ids = False

    # ================= ACTIONS =================

    def action_duyet_luong(self):
        self.write({'trang_thai': 'da_duyet'})

    def action_thanh_toan(self):
        self.write({'trang_thai': 'da_thanh_toan'})

    def action_reset(self):
        self.write({'trang_thai': 'chua_duyet'})
=======
    _description = 'Bảng lương nhân viên'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'thang desc, nam desc'
    _rec_name = 'nhan_vien_id'

    # Thông tin cơ bản
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', related='nhan_vien_id.phong_ban_id', store=True)
    chuc_vu_id = fields.Many2one('chuc_vu', string='Chức vụ', related='nhan_vien_id.chuc_vu_id', store=True)
    
    # Kỳ lương
    thang = fields.Integer(string='Tháng', required=True)
    nam = fields.Integer(string='Năm', required=True)
    ngay_cham = fields.Date(string='Ngày chấm lương', default=fields.Date.today)
    
    # Thông tin công
    so_ngay_cong = fields.Float(string='Số ngày công', default=0)
    so_gio_tang_ca = fields.Float(string='Số giờ tăng ca', default=0)
    ngay_nghi_co_phep = fields.Integer(string='Nghỉ có phép', default=0)
    ngay_nghi_khong_phep = fields.Integer(string='Nghỉ không phép', default=0)
    
    # Lương và phụ cấp
    luong_co_ban = fields.Float(string='Lương cơ bản', required=True)
    phu_cap_chuc_vu = fields.Float(string='Phụ cấp chức vụ', default=0)
    phu_cap_an_trua = fields.Float(string='Phụ cấp ăn trưa', default=0)
    phu_cap_xang_xe = fields.Float(string='Phụ cấp xăng xe', default=0)
    phu_cap_dien_thoai = fields.Float(string='Phụ cấp điện thoại', default=0)
    phu_cap_khac = fields.Float(string='Phụ cấp khác', default=0)
    
    # Tăng ca và thưởng
    tien_tang_ca = fields.Float(string='Tiền tăng ca', compute='_compute_tien_tang_ca', store=True)
    tien_thuong = fields.Float(string='Tiền thưởng', default=0)
    
    # Khấu trừ
    khau_tru_bhxh = fields.Float(string='BHXH (8%)', compute='_compute_khau_tru', store=True)
    khau_tru_bhyt = fields.Float(string='BHYT (1.5%)', compute='_compute_khau_tru', store=True)
    khau_tru_bhtn = fields.Float(string='BHTN (1%)', compute='_compute_khau_tru', store=True)
    khau_tru_thue = fields.Float(string='Thuế TNCN', default=0)
    khau_tru_khac = fields.Float(string='Khấu trừ khác', default=0)
    
    # Tổng hợp
    tong_thu_nhap = fields.Float(string='Tổng thu nhập', compute='_compute_tong_hop', store=True)
    tong_khau_tru = fields.Float(string='Tổng khấu trừ', compute='_compute_tong_hop', store=True)
    thuc_linh = fields.Float(string='Thực lĩnh', compute='_compute_tong_hop', store=True)
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Đang nhập'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('da_chi_tra', 'Đã chi trả')
    ], string='Trạng thái', default='nhap')
    
    ghi_chu = fields.Text(string='Ghi chú')
    
    # Tính giá trị 1 giờ làm việc (8 giờ/ngày, 22 ngày/tháng)
    GIO_LAM_VIEC_TIEU_CHUAN = 176  # 22 ngày * 8 giờ
    
    @api.depends('luong_co_ban', 'so_gio_tang_ca')
    def _compute_tien_tang_ca(self):
        for record in self:
            if record.luong_co_ban and record.so_gio_tang_ca:
                gia_gio = record.luong_co_ban / self.GIO_LAM_VIEC_TIEU_CHUAN
                # Tăng ca thường x 1.5
                record.tien_tang_ca = gia_gio * record.so_gio_tang_ca * 1.5
            else:
                record.tien_tang_ca = 0
    
    @api.depends('luong_co_ban')
    def _compute_khau_tru(self):
        for record in self:
            if record.luong_co_ban:
                record.khau_tru_bhxh = record.luong_co_ban * 0.08
                record.khau_tru_bhyt = record.luong_co_ban * 0.015
                record.khau_tru_bhtn = record.luong_co_ban * 0.01
            else:
                record.khau_tru_bhxh = 0
                record.khau_tru_bhyt = 0
                record.khau_tru_bhtn = 0
    
    @api.depends('luong_co_ban', 'phu_cap_chuc_vu', 'phu_cap_an_trua', 'phu_cap_xang_xe',
                 'phu_cap_dien_thoai', 'phu_cap_khac', 'tien_tang_ca', 'tien_thuong',
                 'khau_tru_bhxh', 'khau_tru_bhyt', 'khau_tru_bhtn', 'khau_tru_thue', 'khau_tru_khac',
                 'so_ngay_cong', 'ngay_nghi_khong_phep')
    def _compute_tong_hop(self):
        for record in self:
            # Tính lương thực tế theo số ngày công
            ngay_cong_thuc_te = record.so_ngay_cong - record.ngay_nghi_khong_phep
            ty_le_luong = ngay_cong_thuc_te / 22 if ngay_cong_thuc_te > 0 else 0
            luong_theo_ngay_cong = record.luong_co_ban * ty_le_luong
            
            # Tổng thu nhập
            record.tong_thu_nhap = (
                luong_theo_ngay_cong +
                record.phu_cap_chuc_vu +
                record.phu_cap_an_trua +
                record.phu_cap_xang_xe +
                record.phu_cap_dien_thoai +
                record.phu_cap_khac +
                record.tien_tang_ca +
                record.tien_thuong
            )
            
            # Tổng khấu trừ
            record.tong_khau_tru = (
                record.khau_tru_bhxh +
                record.khau_tru_bhyt +
                record.khau_tru_bhtn +
                record.khau_tru_thue +
                record.khau_tru_khac
            )
            
            # Thực lĩnh
            record.thuc_linh = record.tong_thu_nhap - record.tong_khau_tru
    
    @api.onchange('nhan_vien_id')
    def _onchange_nhan_vien_id(self):
        """Tự động điền lương cơ bản và phụ cấp từ chức vụ"""
        if self.nhan_vien_id and self.nhan_vien_id.chuc_vu_id:
            self.luong_co_ban = self.nhan_vien_id.chuc_vu_id.luong_co_ban
            self.phu_cap_chuc_vu = self.nhan_vien_id.chuc_vu_id.phu_cap
    
    @api.onchange('thang', 'nam', 'nhan_vien_id')
    def _onchange_thang_nam(self):
        """Tự động lấy thông tin công từ báo cáo chấm công"""
        if self.thang and self.nam and self.nhan_vien_id:
            bao_cao = self.env['bao_cao_cham_cong'].search([
                ('thang', '=', self.thang),
                ('nam', '=', self.nam),
                ('nhan_vien_id', '=', self.nhan_vien_id.id)
            ], limit=1)
            
            if bao_cao:
                self.so_ngay_cong = bao_cao.tong_ngay_cong
                self.so_gio_tang_ca = bao_cao.tong_gio_tang_ca
                self.ngay_nghi_co_phep = bao_cao.ngay_nghi_co_phep
                self.ngay_nghi_khong_phep = bao_cao.ngay_nghi_khong_phep
    
    def action_gui_duyet(self):
        """Gửi bảng lương để duyệt"""
        for record in self:
            if record.trang_thai == 'nhap':
                record.trang_thai = 'cho_duyet'
    
    def action_duyet(self):
        """Duyệt bảng lương"""
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.trang_thai = 'da_duyet'
    
    def action_chi_tra(self):
        """Xác nhận đã chi trả lương"""
        for record in self:
            if record.trang_thai == 'da_duyet':
                record.trang_thai = 'da_chi_tra'
    
    def action_huy_duyet(self):
        """Hủy duyệt, quay về trạng thái nhập"""
        for record in self:
            if record.trang_thai in ['cho_duyet', 'da_duyet']:
                record.trang_thai = 'nhap'
    
    _sql_constraints = [
        ('nhan_vien_thang_nam_unique', 'UNIQUE(nhan_vien_id, thang, nam)', 
         'Đã tồn tại bảng lương cho nhân viên này trong tháng này!')
    ]


class ChiTietKhoanPhuCap(models.Model):
    _name = 'chi_tiet_phu_cap'
    _description = 'Chi tiết các khoản phụ cấp'
    
    bang_luong_id = fields.Many2one('bang_luong', string='Bảng lương', required=True, ondelete='cascade')
    ten_phu_cap = fields.Char(string='Tên phụ cấp', required=True)
    so_tien = fields.Float(string='Số tiền', required=True)
    ghi_chu = fields.Char(string='Ghi chú')


class ChiTietKhoanKhauTru(models.Model):
    _name = 'chi_tiet_khau_tru'
    _description = 'Chi tiết các khoản khấu trừ'
    
    bang_luong_id = fields.Many2one('bang_luong', string='Bảng lương', required=True, ondelete='cascade')
    ten_khau_tru = fields.Char(string='Tên khoản khấu trừ', required=True)
    so_tien = fields.Float(string='Số tiền', required=True)
    ghi_chu = fields.Char(string='Ghi chú')
>>>>>>> cc63fe88 (update)
