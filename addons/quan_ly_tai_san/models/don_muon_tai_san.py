# -*- coding: utf-8 -*-

from odoo import models, fields


class DonMuonTaiSan(models.Model):
    _name = 'don_muon_tai_san'
    _description = 'Chi tiết đơn mượn tài sản'

    phieu_muon_id = fields.Many2one('muon_tra_tai_san', string='Phiếu mượn', required=True, ondelete='cascade')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True)
    so_luong = fields.Integer(string='Số lượng', default=1)
    tinh_trang_muon = fields.Text(string='Tình trạng khi mượn')
    tinh_trang_tra = fields.Text(string='Tình trạng khi trả')
    ghi_chu = fields.Text(string='Ghi chú')
