# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Chức vụ'
    _rec_name = 'ten_chuc_vu'
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

    ten_chuc_vu = fields.Char(
        string="Tên chức vụ",
        required=True,
        index=True
    )
    
    cap_bac = fields.Selection(
        selection=[
            ('nhan_vien', 'Nhân viên'),
            ('truong_nhom', 'Trưởng nhóm'),
            ('truong_phong', 'Trưởng phòng'),
            ('pho_giam_doc', 'Phó giám đốc'),
            ('giam_doc', 'Giám đốc'),
        ],
        string="Cấp bậc"
    )

    mo_ta = fields.Text(
        string="Mô tả"
    )

    luong_co_ban = fields.Float(
        string="Lương cơ bản",
        digits=(16, 0)
    )

    phong_ban_id = fields.Many2one(
        comodel_name='phong_ban',
        string="Phòng ban"
    )

    nhan_vien_ids = fields.One2many(
        comodel_name='nhan_vien',
        inverse_name='chuc_vu_id',
        string='Nhân viên'
    )
    
    so_luong_nhan_vien = fields.Integer(
        string="Số lượng nhân viên",
        compute='_compute_so_luong_nhan_vien',
        store=True
    )

    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )

    @api.depends('nhan_vien_ids')
    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_nhan_vien = len(record.nhan_vien_ids)

    @api.constrains('luong_co_ban')
    def _check_luong_co_ban(self):
        for record in self:
            if record.luong_co_ban and record.luong_co_ban < 0:
                raise ValidationError('Lương cơ bản phải lớn hơn 0!')
