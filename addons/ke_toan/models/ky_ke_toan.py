# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class KyKeToan(models.Model):
    """Kỳ kế toán (tháng/quý/năm)"""
    _name = 'ke_toan.ky'
    _description = 'Kỳ kế toán'
    _rec_name = 'ten_ky'
    _order = 'ngay_bat_dau desc'

    ten_ky = fields.Char(string='Tên kỳ', required=True)
    loai_ky = fields.Selection([
        ('thang', 'Tháng'),
        ('quy', 'Quý'),
        ('nam', 'Năm'),
    ], string='Loại kỳ', required=True, default='thang')
    
    ngay_bat_dau = fields.Date(string='Ngày bắt đầu', required=True)
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc', required=True)
    
    nam_tai_chinh = fields.Integer(string='Năm tài chính', required=True,
                                    default=lambda self: fields.Date.today().year)
    thang = fields.Integer(string='Tháng')
    quy = fields.Integer(string='Quý')
    
    trang_thai = fields.Selection([
        ('mo', 'Đang mở'),
        ('dong', 'Đã đóng'),
        ('khoa', 'Đã khóa'),
    ], string='Trạng thái', default='mo', required=True)
    
    # Thống kê
    so_but_toan = fields.Integer(string='Số bút toán', compute='_compute_thong_ke')
    tong_phat_sinh_no = fields.Float(string='Tổng phát sinh Nợ', compute='_compute_thong_ke')
    tong_phat_sinh_co = fields.Float(string='Tổng phát sinh Có', compute='_compute_thong_ke')
    
    but_toan_ids = fields.One2many('ke_toan.but_toan', 'ky_ke_toan_id', string='Bút toán')
    
    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('but_toan_ids', 'but_toan_ids.trang_thai')
    def _compute_thong_ke(self):
        for record in self:
            but_toan_da_ghi = record.but_toan_ids.filtered(lambda b: b.trang_thai == 'da_ghi_so')
            record.so_but_toan = len(but_toan_da_ghi)
            record.tong_phat_sinh_no = sum(but_toan_da_ghi.mapped('tong_no'))
            record.tong_phat_sinh_co = sum(but_toan_da_ghi.mapped('tong_co'))

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError('Ngày bắt đầu phải nhỏ hơn ngày kết thúc!')

    @api.onchange('loai_ky', 'nam_tai_chinh', 'thang', 'quy')
    def _onchange_tinh_ngay(self):
        if self.loai_ky == 'thang' and self.thang and self.nam_tai_chinh:
            self.ngay_bat_dau = fields.Date.today().replace(
                year=self.nam_tai_chinh, month=self.thang, day=1
            )
            self.ngay_ket_thuc = self.ngay_bat_dau + relativedelta(months=1, days=-1)
            self.ten_ky = f"Tháng {self.thang}/{self.nam_tai_chinh}"
        elif self.loai_ky == 'quy' and self.quy and self.nam_tai_chinh:
            thang_dau = (self.quy - 1) * 3 + 1
            self.ngay_bat_dau = fields.Date.today().replace(
                year=self.nam_tai_chinh, month=thang_dau, day=1
            )
            self.ngay_ket_thuc = self.ngay_bat_dau + relativedelta(months=3, days=-1)
            self.ten_ky = f"Quý {self.quy}/{self.nam_tai_chinh}"
        elif self.loai_ky == 'nam' and self.nam_tai_chinh:
            self.ngay_bat_dau = fields.Date.today().replace(
                year=self.nam_tai_chinh, month=1, day=1
            )
            self.ngay_ket_thuc = fields.Date.today().replace(
                year=self.nam_tai_chinh, month=12, day=31
            )
            self.ten_ky = f"Năm {self.nam_tai_chinh}"

    def action_dong_ky(self):
        """Đóng kỳ kế toán"""
        for record in self:
            if record.trang_thai == 'mo':
                record.trang_thai = 'dong'
        return True

    def action_khoa_ky(self):
        """Khóa kỳ kế toán - không cho chỉnh sửa"""
        for record in self:
            if record.trang_thai == 'dong':
                record.trang_thai = 'khoa'
        return True

    def action_mo_lai(self):
        """Mở lại kỳ kế toán"""
        for record in self:
            if record.trang_thai in ['dong', 'khoa']:
                record.trang_thai = 'mo'
        return True
