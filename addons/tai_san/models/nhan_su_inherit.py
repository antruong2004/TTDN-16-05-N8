# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NhanVienInherit(models.Model):
    _inherit = 'nhan_vien'

    tai_san_quan_ly_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='nguoi_quan_ly_id',
        string='Tài sản quản lý'
    )
    
    so_luong_tai_san_quan_ly = fields.Integer(
        string="Số lượng tài sản",
        compute='_compute_so_luong_tai_san_quan_ly',
        store=True
    )

    @api.depends('tai_san_quan_ly_ids')
    def _compute_so_luong_tai_san_quan_ly(self):
        for record in self:
            record.so_luong_tai_san_quan_ly = len(record.tai_san_quan_ly_ids)


class PhongBanInherit(models.Model):
    _inherit = 'phong_ban'

    tai_san_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='phong_ban_id',
        string='Tài sản của phòng ban'
    )
    
    so_luong_tai_san = fields.Integer(
        string="Số lượng tài sản",
        compute='_compute_so_luong_tai_san',
        store=True
    )
    
    tong_gia_tri_tai_san = fields.Float(
        string="Tổng giá trị tài sản",
        compute='_compute_tong_gia_tri_tai_san',
        digits=(16, 2)
    )

    @api.depends('tai_san_ids')
    def _compute_so_luong_tai_san(self):
        for record in self:
            record.so_luong_tai_san = len(record.tai_san_ids)
    
    @api.depends('tai_san_ids.gia_tri_con_lai')
    def _compute_tong_gia_tri_tai_san(self):
        for record in self:
            record.tong_gia_tri_tai_san = sum(record.tai_san_ids.mapped('gia_tri_con_lai'))
