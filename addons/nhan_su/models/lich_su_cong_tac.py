# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Lịch sử công tác'
    _order = 'ngay_bat_dau desc'

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    chuc_vu_id = fields.Many2one(
        comodel_name='chuc_vu',
        string="Chức vụ",
        required=True
    )

    phong_ban_id = fields.Many2one(
        comodel_name='phong_ban',
        string="Phòng ban",
        required=True
    )

    ngay_bat_dau = fields.Date(
        string="Ngày bắt đầu",
        required=True,
        default=fields.Date.context_today
    )

    ngay_ket_thuc = fields.Date(
        string="Ngày kết thúc"
    )
    
    thoi_gian_cong_tac = fields.Integer(
        string="Thời gian công tác (ngày)",
        compute='_compute_thoi_gian_cong_tac',
        store=True
    )

    ly_do_thay_doi = fields.Text(
        string="Lý do thay đổi"
    )

    ghi_chu = fields.Text(
        string="Ghi chú"
    )

    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_thoi_gian_cong_tac(self):
        for record in self:
            if record.ngay_bat_dau:
                ngay_cuoi = record.ngay_ket_thuc or date.today()
                record.thoi_gian_cong_tac = (ngay_cuoi - record.ngay_bat_dau).days
            else:
                record.thoi_gian_cong_tac = 0

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau and record.ngay_ket_thuc <= record.ngay_bat_dau:
                raise ValidationError('Ngày kết thúc phải sau ngày bắt đầu!')
