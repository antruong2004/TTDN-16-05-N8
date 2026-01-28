# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MuonTraTaiSan(models.Model):
    _name = 'muon_tra_tai_san'
    _description = 'Mượn/trả tài sản'
    _rec_name = 'ma_phieu'

    ma_phieu = fields.Char(string='Mã phiếu', required=True, copy=False, readonly=True,
                          default=lambda self: self.env['ir.sequence'].next_by_code('muon_tra_tai_san') or 'New')
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên mượn', required=True)
    ngay_muon = fields.Date(string='Ngày mượn', required=True, default=fields.Date.context_today)
    ngay_tra_du_kien = fields.Date(string='Ngày trả dự kiến')
    ngay_tra_thuc_te = fields.Date(string='Ngày trả thực tế')
    ly_do = fields.Text(string='Lý do mượn', required=True)
    chi_tiet_ids = fields.One2many('don_muon_tai_san', 'phieu_muon_id', string='Chi tiết tài sản')
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả'),
        ('tu_choi', 'Từ chối'),
    ], string='Trạng thái', default='nhap', required=True)
    nguoi_duyet_id = fields.Many2one('nhan_vien', string='Người duyệt')
    ngay_duyet = fields.Date(string='Ngày duyệt')
    ghi_chu = fields.Text(string='Ghi chú')

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('muon_tra_tai_san') or 'MT001'
        return super(MuonTraTaiSan, self).create(vals)

    # ========== WORKFLOW ACTIONS ==========
    def action_gui_duyet(self):
        """Gửi phiếu mượn để duyệt"""
        for record in self:
            if record.trang_thai == 'nhap':
                record.trang_thai = 'cho_duyet'
        return True

    def action_duyet(self):
        """Duyệt phiếu mượn"""
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({
                    'trang_thai': 'da_duyet',
                    'nguoi_duyet_id': self.env.user.id if hasattr(self.env.user, 'nhan_vien_id') else False,
                    'ngay_duyet': fields.Date.context_today(self)
                })
        return True

    def action_tu_choi(self):
        """Từ chối phiếu mượn"""
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.trang_thai = 'tu_choi'
        return True

    def action_nhap_lai(self):
        """Đưa về trạng thái nháp để sửa"""
        for record in self:
            if record.trang_thai == 'tu_choi':
                record.trang_thai = 'nhap'
        return True

    def action_bat_dau_muon(self):
        """Bắt đầu mượn tài sản"""
        for record in self:
            if record.trang_thai == 'da_duyet':
                record.trang_thai = 'dang_muon'
                # TODO: Cập nhật trạng thái tài sản nếu cần
        return True

    def action_tra_tai_san(self):
        """Trả tài sản"""
        for record in self:
            if record.trang_thai == 'dang_muon':
                record.write({
                    'trang_thai': 'da_tra',
                    'ngay_tra_thuc_te': fields.Date.context_today(self)
                })
        return True
