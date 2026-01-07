# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Chứng chỉ'
    _order = 'ngay_cap desc'

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    ten_chung_chi = fields.Char(
        string="Tên chứng chỉ",
        required=True
    )

    co_quan_cap = fields.Char(
        string="Cơ quan cấp"
    )

    ngay_cap = fields.Date(
        string="Ngày cấp",
        required=True,
        default=fields.Date.context_today
    )

    ngay_het_han = fields.Date(
        string="Ngày hết hạn"
    )
    
    con_hieu_luc = fields.Boolean(
        string="Còn hiệu lực",
        compute='_compute_con_hieu_luc',
        store=True
    )

    so_hieu_chung_chi = fields.Char(
        string="Số hiệu chứng chỉ"
    )

    cap_do = fields.Selection(
        selection=[
            ('cap_hanh', 'Cấp hành'),
            ('cap_tinh', 'Cấp tỉnh'),
            ('cap_quoc_gia', 'Cấp quốc gia'),
            ('cap_quoc_te', 'Cấp quốc tế'),
        ],
        string="Cấp độ"
    )

    diem = fields.Float(
        string="Điểm"
    )

    mo_ta = fields.Text(
        string="Mô tả"
    )

    attachment_id = fields.Many2many(
        comodel_name='ir.attachment',
        string='Tài liệu đính kèm'
    )

    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )

    @api.depends('ngay_het_han')
    def _compute_con_hieu_luc(self):
        for record in self:
            if record.ngay_het_han:
                record.con_hieu_luc = record.ngay_het_han >= date.today()
            else:
                record.con_hieu_luc = True

    @api.constrains('ngay_cap', 'ngay_het_han')
    def _check_ngay(self):
        for record in self:
            if record.ngay_cap and record.ngay_cap > date.today():
                raise ValidationError('Ngày cấp không được là ngày trong tương lai!')
            if record.ngay_het_han and record.ngay_cap and record.ngay_het_han <= record.ngay_cap:
                raise ValidationError('Ngày hết hạn phải sau ngày cấp!')
