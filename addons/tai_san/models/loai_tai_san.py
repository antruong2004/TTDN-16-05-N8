# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LoaiTaiSan(models.Model):
    _name = 'loai_tai_san'
    _description = 'Loại tài sản'
    _rec_name = 'ten_loai'
    _order = 'ma_loai asc'
    
    _sql_constraints = [
        ('ma_loai_unique', 'unique(ma_loai)', 'Mã loại tài sản phải là duy nhất!'),
    ]

    ma_loai = fields.Char(
        string="Mã loại",
        required=True,
        copy=False,
        index=True
    )
    
    ten_loai = fields.Char(
        string="Tên loại tài sản",
        required=True,
        index=True
    )
    
    thoi_gian_khau_hao = fields.Integer(
        string="Thời gian khấu hao (tháng)",
        required=True,
        default=60,
        help="Số tháng khấu hao cho loại tài sản này"
    )
    
    ty_le_khau_hao_nam = fields.Float(
        string="Tỷ lệ khấu hao năm (%)",
        compute='_compute_ty_le_khau_hao',
        store=True,
        help="Tỷ lệ khấu hao hàng năm tính theo phần trăm"
    )
    
    phuong_phap_khau_hao = fields.Selection(
        selection=[
            ('duong_thang', 'Khấu hao đường thẳng'),
            ('so_du_giam_dan', 'Khấu hao số dư giảm dần'),
        ],
        string="Phương pháp khấu hao",
        default='duong_thang',
        required=True
    )
    
    he_so_khau_hao = fields.Float(
        string="Hệ số khấu hao",
        default=2.0,
        help="Hệ số tăng tốc cho khấu hao số dư giảm dần (thường 1.5, 2.0 hoặc 2.5)"
    )
    
    mo_ta = fields.Text(string="Mô tả")
    
    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )
    
    tai_san_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='loai_tai_san_id',
        string='Tài sản'
    )
    
    so_luong_tai_san = fields.Integer(
        string="Số lượng tài sản",
        compute='_compute_so_luong_tai_san',
        store=True
    )

    @api.depends('thoi_gian_khau_hao')
    def _compute_ty_le_khau_hao(self):
        for record in self:
            if record.thoi_gian_khau_hao > 0:
                record.ty_le_khau_hao_nam = (12.0 / record.thoi_gian_khau_hao) * 100
            else:
                record.ty_le_khau_hao_nam = 0.0

    @api.depends('tai_san_ids')
    def _compute_so_luong_tai_san(self):
        for record in self:
            record.so_luong_tai_san = len(record.tai_san_ids)

    @api.constrains('thoi_gian_khau_hao')
    def _check_thoi_gian_khau_hao(self):
        for record in self:
            if record.thoi_gian_khau_hao <= 0:
                raise ValidationError(_('Thời gian khấu hao phải lớn hơn 0!'))
