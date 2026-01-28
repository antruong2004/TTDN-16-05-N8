# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Tài sản cố định'
    _rec_name = 'ten_tai_san'
    _order = 'ngay_mua desc'

    ma_tai_san = fields.Char(string='Mã tài sản', required=True, copy=False, readonly=True,
                             default=lambda self: self.env['ir.sequence'].next_by_code('tai_san') or 'New')
    ten_tai_san = fields.Char(string='Tên tài sản', required=True, tracking=True)
    danh_muc_id = fields.Many2one('danh_muc_tai_san', string='Danh mục', required=True, ondelete='restrict')
    
    # Thông tin tài chính
    gia_tri_ban_dau = fields.Float(string='Giá trị ban đầu', required=True, default=0.0)
    gia_tri_con_lai = fields.Float(string='Giá trị còn lại', compute='_compute_gia_tri_con_lai', store=True)
    tong_khau_hao = fields.Float(string='Tổng khấu hao', compute='_compute_tong_khau_hao', store=True)
    ty_le_khau_hao_hien_tai = fields.Float(string='% Khấu hao', compute='_compute_ty_le_khau_hao', store=True)
    
    # Thông tin mua sắm
    ngay_mua = fields.Date(string='Ngày mua', default=fields.Date.context_today, required=True)
    ngay_bat_dau_su_dung = fields.Date(string='Ngày bắt đầu sử dụng', required=True)
    noi_mua = fields.Char(string='Nơi mua')
    so_hoa_don = fields.Char(string='Số hóa đơn')
    nha_cung_cap = fields.Char(string='Nhà cung cấp')
    
    # Khấu hao
    phuong_phap_khau_hao = fields.Selection([
        ('duong_thang', 'Đường thẳng'),
        ('so_du_giam_dan', 'Số dư giảm dần'),
        ('tong_so_nam', 'Tổng số năm sử dụng'),
    ], string='Phương pháp khấu hao', default='duong_thang', required=True)
    thoi_gian_su_dung = fields.Integer(string='Thời gian sử dụng (tháng)', related='danh_muc_id.thoi_gian_su_dung', store=True)
    ty_le_khau_hao = fields.Float(string='Tỷ lệ khấu hao (%)', related='danh_muc_id.ty_le_khau_hao', store=True)
    khau_hao_ids = fields.One2many('khau_hao', 'tai_san_id', string='Lịch sử khấu hao')
    
    # Quản lý
    nguoi_quan_ly_id = fields.Many2one('nhan_vien', string='Người quản lý')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban sử dụng')
    vi_tri = fields.Char(string='Vị trí')
    
    # Bảo hành
    ngay_het_bao_hanh = fields.Date(string='Ngày hết bảo hành')
    thoi_gian_bao_hanh = fields.Integer(string='Thời gian bảo hành (tháng)', default=12)
    con_bao_hanh = fields.Boolean(string='Còn bảo hành', compute='_compute_con_bao_hanh', store=True)
    
    # Thông số kỹ thuật
    serial_number = fields.Char(string='Serial Number')
    model = fields.Char(string='Model/Phiên bản')
    xuat_xu = fields.Char(string='Xuất xứ')
    nam_san_xuat = fields.Integer(string='Năm sản xuất')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('bao_tri', 'Bảo trì'),
        ('hong', 'Hỏng'),
        ('thanh_ly', 'Đã thanh lý'),
    ], string='Trạng thái', default='moi', required=True)
    
    muc_do_su_dung = fields.Selection([
        ('tot', 'Tốt (80-100%)'),
        ('kha', 'Khá (60-80%)'),
        ('trung_binh', 'Trung bình (40-60%)'),
        ('kem', 'Kém (20-40%)'),
        ('xuong_cap', 'Xuống cấp (<20%)'),
    ], string='Mức độ sử dụng', default='tot')
    
    # Ghi chú
    mo_ta = fields.Text(string='Mô tả')
    ghi_chu = fields.Text(string='Ghi chú')
    active = fields.Boolean(string='Đang hoạt động', default=True)
    
    # Computed fields nâng cao
    so_ngay_su_dung = fields.Integer(string='Số ngày đã sử dụng', compute='_compute_so_ngay_su_dung', store=True)
    tuoi_tai_san = fields.Char(string='Tuổi tài sản', compute='_compute_tuoi_tai_san')

    @api.depends('gia_tri_ban_dau', 'khau_hao_ids.gia_tri_khau_hao')
    def _compute_gia_tri_con_lai(self):
        for record in self:
            tong_khau_hao = sum(record.khau_hao_ids.mapped('gia_tri_khau_hao'))
            record.gia_tri_con_lai = record.gia_tri_ban_dau - tong_khau_hao

    @api.depends('khau_hao_ids.gia_tri_khau_hao')
    def _compute_tong_khau_hao(self):
        for record in self:
            record.tong_khau_hao = sum(record.khau_hao_ids.mapped('gia_tri_khau_hao'))

    @api.depends('gia_tri_ban_dau', 'tong_khau_hao')
    def _compute_ty_le_khau_hao(self):
        for record in self:
            if record.gia_tri_ban_dau > 0:
                record.ty_le_khau_hao_hien_tai = (record.tong_khau_hao / record.gia_tri_ban_dau) * 100
            else:
                record.ty_le_khau_hao_hien_tai = 0.0

    @api.depends('ngay_het_bao_hanh')
    def _compute_con_bao_hanh(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.ngay_het_bao_hanh:
                record.con_bao_hanh = record.ngay_het_bao_hanh >= today
            else:
                record.con_bao_hanh = False

    @api.depends('ngay_bat_dau_su_dung')
    def _compute_so_ngay_su_dung(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.ngay_bat_dau_su_dung:
                delta = today - record.ngay_bat_dau_su_dung
                record.so_ngay_su_dung = delta.days
            else:
                record.so_ngay_su_dung = 0

    @api.depends('ngay_bat_dau_su_dung')
    def _compute_tuoi_tai_san(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.ngay_bat_dau_su_dung:
                delta = today - record.ngay_bat_dau_su_dung
                nam = delta.days // 365
                thang = (delta.days % 365) // 30
                record.tuoi_tai_san = f"{nam} năm {thang} tháng"
            else:
                record.tuoi_tai_san = "Chưa sử dụng"

    @api.onchange('ngay_mua', 'thoi_gian_bao_hanh')
    def _onchange_tinh_ngay_het_bao_hanh(self):
        if self.ngay_mua and self.thoi_gian_bao_hanh:
            from dateutil.relativedelta import relativedelta
            self.ngay_het_bao_hanh = self.ngay_mua + relativedelta(months=self.thoi_gian_bao_hanh)

    @api.model
    def create(self, vals):
        if vals.get('ma_tai_san', 'New') == 'New':
            vals['ma_tai_san'] = self.env['ir.sequence'].next_by_code('tai_san') or 'TS001'
        return super(TaiSan, self).create(vals)

    _sql_constraints = [
        ('ma_tai_san_unique', 'unique(ma_tai_san)', 'Mã tài sản phải duy nhất!'),
        ('gia_tri_ban_dau_positive', 'check(gia_tri_ban_dau >= 0)', 'Giá trị ban đầu phải >= 0!')
    ]

    # ========== WORKFLOW ACTIONS ==========
    def action_bat_dau_su_dung(self):
        """Chuyển trạng thái sang đang sử dụng"""
        for record in self:
            if record.trang_thai == 'moi':
                record.trang_thai = 'dang_su_dung'
        return True

    def action_bao_tri(self):
        """Chuyển sang trạng thái bảo trì"""
        for record in self:
            if record.trang_thai in ['dang_su_dung', 'hong']:
                record.trang_thai = 'bao_tri'
        return True

    def action_sua_chua_xong(self):
        """Hoàn thành bảo trì, quay lại trạng thái đang sử dụng"""
        for record in self:
            if record.trang_thai == 'bao_tri':
                record.trang_thai = 'dang_su_dung'
        return True

    def action_hong(self):
        """Báo hỏng tài sản"""
        for record in self:
            if record.trang_thai in ['dang_su_dung', 'bao_tri']:
                record.trang_thai = 'hong'
        return True
