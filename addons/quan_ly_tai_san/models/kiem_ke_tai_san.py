# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KiemKeTaiSan(models.Model):
    _name = 'kiem_ke_tai_san'
    _description = 'Kiểm kê tài sản'
    _rec_name = 'ma_phieu'

    ma_phieu = fields.Char(string='Mã phiếu', required=True, copy=False, readonly=True,
                          default=lambda self: self.env['ir.sequence'].next_by_code('kiem_ke_tai_san') or 'New')
    ten_dot_kiem_ke = fields.Char(string='Tên đợt kiểm kê', required=True)
    ngay_bat_dau = fields.Date(string='Ngày bắt đầu', required=True, default=fields.Date.context_today)
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc', required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban kiểm kê')
    chi_tiet_ids = fields.One2many('chi_tiet_kiem_ke', 'kiem_ke_id', string='Chi tiết kiểm kê')
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('dang_kiem_ke', 'Đang kiểm kê'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Đã hủy'),
    ], string='Trạng thái', default='nhap', required=True)
    ghi_chu = fields.Text(string='Ghi chú')

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('kiem_ke_tai_san') or 'KK001'
        return super(KiemKeTaiSan, self).create(vals)

    # ========== WORKFLOW ACTIONS ==========
    def action_bat_dau_kiem_ke(self):
        """Bắt đầu kiểm kê"""
        for record in self:
            if record.trang_thai == 'nhap':
                record.trang_thai = 'dang_kiem_ke'
        return True

    def action_hoan_thanh(self):
        """Hoàn thành kiểm kê"""
        for record in self:
            if record.trang_thai == 'dang_kiem_ke':
                record.trang_thai = 'hoan_thanh'
        return True

    def action_huy(self):
        """Hủy đợt kiểm kê"""
        for record in self:
            if record.trang_thai in ['nhap', 'dang_kiem_ke']:
                record.trang_thai = 'huy'
        return True
