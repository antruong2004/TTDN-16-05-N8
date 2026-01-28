# -*- coding: utf-8 -*-

from odoo import models, fields


class LichSuKhauHao(models.Model):
    _name = 'lich_su_khau_hao'
    _description = 'Lịch sử khấu hao'
    _order = 'ngay_ghi_nhan desc'

    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    khau_hao_id = fields.Many2one('khau_hao', string='Khấu hao', ondelete='cascade')
    ngay_ghi_nhan = fields.Date(string='Ngày ghi nhận', required=True, default=fields.Date.context_today)
    gia_tri_khau_hao = fields.Float(string='Giá trị khấu hao', required=True)
    gia_tri_con_lai = fields.Float(string='Giá trị còn lại')
    ghi_chu = fields.Text(string='Ghi chú')
