# -*- coding: utf-8 -*-

from odoo import models, fields, api
from calendar import monthrange


class BangLuong(models.Model):
    _name = 'bang_luong'
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
