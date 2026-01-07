# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NhanVienInherit(models.Model):
    _inherit = 'nhan_vien'

    so_cai_lap_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='nguoi_lap_id',
        string='Chứng từ đã lập'
    )
    
    so_cai_duyet_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='nguoi_duyet_id',
        string='Chứng từ đã duyệt'
    )
    
    so_luong_chung_tu_lap = fields.Integer(
        string="Số chứng từ đã lập",
        compute='_compute_so_luong_chung_tu',
        store=True
    )
    
    so_luong_chung_tu_duyet = fields.Integer(
        string="Số chứng từ đã duyệt",
        compute='_compute_so_luong_chung_tu',
        store=True
    )

    @api.depends('so_cai_lap_ids', 'so_cai_duyet_ids')
    def _compute_so_luong_chung_tu(self):
        for record in self:
            record.so_luong_chung_tu_lap = len(record.so_cai_lap_ids)
            record.so_luong_chung_tu_duyet = len(record.so_cai_duyet_ids)


class PhongBanInherit(models.Model):
    _inherit = 'phong_ban'

    so_cai_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='phong_ban_id',
        string='Chứng từ của phòng ban'
    )
    
    so_luong_chung_tu = fields.Integer(
        string="Số chứng từ",
        compute='_compute_so_luong_chung_tu',
        store=True
    )
    
    tong_gia_tri_chung_tu = fields.Float(
        string="Tổng giá trị chứng từ",
        compute='_compute_tong_gia_tri_chung_tu',
        digits=(16, 2)
    )

    @api.depends('so_cai_ids')
    def _compute_so_luong_chung_tu(self):
        for record in self:
            record.so_luong_chung_tu = len(record.so_cai_ids)
    
    @api.depends('so_cai_ids.so_tien')
    def _compute_tong_gia_tri_chung_tu(self):
        for record in self:
            record.tong_gia_tri_chung_tu = sum(record.so_cai_ids.mapped('so_tien'))
