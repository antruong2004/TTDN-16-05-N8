# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DanhMucTaiSan(models.Model):
    _name = 'danh_muc_tai_san'
    _description = 'Danh mục tài sản cố định'
    _rec_name = 'ten_danh_muc'

    ma_danh_muc = fields.Char(string='Mã danh mục', required=True, copy=False)
    ten_danh_muc = fields.Char(string='Tên danh mục', required=True)
    mo_ta = fields.Text(string='Mô tả')
    thoi_gian_su_dung = fields.Integer(string='Thời gian sử dụng (tháng)', default=60,
                                      help='Thời gian sử dụng ước tính tính bằng tháng')
    ty_le_khau_hao = fields.Float(string='Tỷ lệ khấu hao (%/năm)', default=10.0,
                                   help='Tỷ lệ khấu hao hằng năm theo %')
    so_luong_tai_san = fields.Integer(string='Số lượng tài sản', compute='_compute_so_luong_tai_san')
    active = fields.Boolean(string='Đang hoạt động', default=True)
    
    _sql_constraints = [
        ('ma_danh_muc_unique', 'unique(ma_danh_muc)', 'Mã danh mục phải duy nhất!')
    ]

    def _compute_so_luong_tai_san(self):
        """Tính số lượng tài sản trong danh mục"""
        for record in self:
            record.so_luong_tai_san = self.env['tai_san'].search_count([
                ('danh_muc_id', '=', record.id)
            ])
