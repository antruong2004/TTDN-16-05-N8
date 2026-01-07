from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Phòng ban'
    _rec_name = 'ten_phong_ban'
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

    ten_phong_ban = fields.Char(
        string="Tên phòng ban",
        required=True,
        index=True
    )
    
    truong_phong_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Trưởng phòng"
    )

    mo_ta = fields.Text(
        string="Mô tả"
    )

    nhan_vien_ids = fields.Many2many(
        comodel_name='nhan_vien',
        relation='phong_ban_nhan_vien_rel',
        column1='phong_ban_id',
        column2='nhan_vien_id',
        string='Danh sách nhân viên'
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
