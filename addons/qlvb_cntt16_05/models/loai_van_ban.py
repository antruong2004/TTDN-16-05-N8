# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _description = 'Loại văn bản'
    _rec_name = 'ten_loai_van_ban'


    _order = 'ma_dinh_danh asc'
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất!'),
    ]

    ma_dinh_danh = fields.Char(
        string="Mã định danh",
        required=True,
        copy=False,
        index=True
    )

    ten_loai_van_ban = fields.Char(
        string="Tên loại văn bản",
        required=True,
        index=True
    )

    mo_ta = fields.Text(
        string="Mô tả"
    )

    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )

    # Uncomment sau khi tạo model van_ban
    # van_ban_ids = fields.One2many(
    #     comodel_name='van_ban',
    #     inverse_name='loai_van_ban_id',
    #     string='Văn bản'
    # )
    
    # so_luong_van_ban = fields.Integer(
    #     string="Số lượng văn bản",
    #     compute='_compute_so_luong_van_ban',
    #     store=True
    # )

    # @api.depends('van_ban_ids')
    # def _compute_so_luong_van_ban(self):
    #     for record in self:
    #         record.so_luong_van_ban = len(record.van_ban_ids)
