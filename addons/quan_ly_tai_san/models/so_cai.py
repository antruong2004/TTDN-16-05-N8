# -*- coding: utf-8 -*-

from odoo import models, fields


class SoCai(models.Model):
    _name = 'so_cai'
    _description = 'Sổ cái kế toán'
    _rec_name = 'so_chung_tu'
    _order = 'ngay_chung_tu desc'

    so_chung_tu = fields.Char(string='Số chứng từ', required=True, copy=False)
    ngay_chung_tu = fields.Date(string='Ngày chứng từ', required=True, default=fields.Date.context_today)
    loai_chung_tu = fields.Selection([
        ('mua_sam', 'Mua sắm'),
        ('khau_hao', 'Khấu hao'),
        ('thanh_ly', 'Thanh lý'),
        ('dieu_chinh', 'Điều chỉnh'),
    ], string='Loại chứng từ', required=True, default='khau_hao')
    
    tai_khoan_no_id = fields.Many2one('tai_khoan_ke_toan', string='TK Nợ')
    tai_khoan_co_id = fields.Many2one('tai_khoan_ke_toan', string='TK Có')
    so_tien = fields.Float(string='Số tiền', required=True, default=0.0)
    
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', ondelete='cascade')
    dien_giai = fields.Text(string='Diễn giải')
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_ghi_so', 'Đã ghi sổ'),
        ('huy', 'Đã hủy'),
    ], string='Trạng thái', default='nhap', required=True)

    _sql_constraints = [
        ('so_tien_positive', 'check(so_tien >= 0)', 'Số tiền phải >= 0!')
    ]
