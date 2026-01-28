# -*- coding: utf-8 -*-

from odoo import models, fields


class TaiKhoanKeToan(models.Model):
    _name = 'tai_khoan_ke_toan'
    _description = 'Tài khoản kế toán'
    _rec_name = 'ten_tai_khoan'

    ma_tai_khoan = fields.Char(string='Mã tài khoản', required=True, copy=False)
    ten_tai_khoan = fields.Char(string='Tên tài khoản', required=True)
    loai_tai_khoan = fields.Selection([
        ('nguyen_gia', 'Nguyên giá TSCĐ'),
        ('khau_hao', 'Khấu hao luỹ kế'),
        ('chi_phi', 'Chi phí khấu hao'),
        ('thu_chi', 'Thu chi khác'),
    ], string='Loại tài khoản', required=True, default='nguyen_gia')
    mo_ta = fields.Text(string='Mô tả')
    active = fields.Boolean(string='Đang sử dụng', default=True)

    _sql_constraints = [
        ('ma_tai_khoan_unique', 'unique(ma_tai_khoan)', 'Mã tài khoản phải duy nhất!')
    ]
