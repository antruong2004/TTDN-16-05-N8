# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LuanChuyenTaiSan(models.Model):
    _name = 'luan_chuyen_tai_san'
    _description = 'Luân chuyển tài sản'
    _rec_name = 'ma_phieu'

    ma_phieu = fields.Char(string='Mã phiếu', required=True, copy=False, readonly=True,
                          default=lambda self: self.env['ir.sequence'].next_by_code('luan_chuyen_tai_san') or 'New')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True)
    ngay_luan_chuyen = fields.Date(string='Ngày luân chuyển', required=True, default=fields.Date.context_today)
    
    # Từ
    phong_ban_cu_id = fields.Many2one('phong_ban', string='Phòng ban cũ')
    nhan_vien_cu_id = fields.Many2one('nhan_vien', string='Nhân viên cũ')
    vi_tri_cu = fields.Char(string='Vị trí cũ')
    
    # Đến
    phong_ban_moi_id = fields.Many2one('phong_ban', string='Phòng ban mới', required=True)
    nhan_vien_moi_id = fields.Many2one('nhan_vien', string='Nhân viên mới')
    vi_tri_moi = fields.Char(string='Vị trí mới')
    
    ly_do = fields.Text(string='Lý do luân chuyển', required=True)
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('hoan_thanh', 'Hoàn thành'),
        ('tu_choi', 'Từ chối'),
    ], string='Trạng thái', default='nhap', required=True)
    nguoi_duyet_id = fields.Many2one('nhan_vien', string='Người duyệt')
    ngay_duyet = fields.Date(string='Ngày duyệt')
    ghi_chu = fields.Text(string='Ghi chú')

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('luan_chuyen_tai_san') or 'LC001'
        return super(LuanChuyenTaiSan, self).create(vals)

    @api.onchange('tai_san_id')
    def _onchange_tai_san_id(self):
        if self.tai_san_id:
            self.phong_ban_cu_id = self.tai_san_id.phong_ban_id
            self.nhan_vien_cu_id = self.tai_san_id.nguoi_quan_ly_id
            self.vi_tri_cu = self.tai_san_id.vi_tri

    # ========== WORKFLOW ACTIONS ==========
    def action_gui_duyet(self):
        """Gửi phiếu luân chuyển để duyệt"""
        for record in self:
            if record.trang_thai == 'nhap':
                record.trang_thai = 'cho_duyet'
        return True

    def action_duyet(self):
        """Duyệt phiếu luân chuyển"""
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({
                    'trang_thai': 'da_duyet',
                    'nguoi_duyet_id': self.env.user.id if hasattr(self.env.user, 'nhan_vien_id') else False,
                    'ngay_duyet': fields.Date.context_today(self)
                })
        return True

    def action_tu_choi(self):
        """Từ chối phiếu luân chuyển"""
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

    def action_hoan_thanh(self):
        """Hoàn thành luân chuyển - cập nhật thông tin tài sản"""
        for record in self:
            if record.trang_thai == 'da_duyet':
                record.tai_san_id.write({
                    'phong_ban_id': record.phong_ban_moi_id.id,
                    'nguoi_quan_ly_id': record.nhan_vien_moi_id.id if record.nhan_vien_moi_id else False,
                    'vi_tri': record.vi_tri_moi
                })
                record.trang_thai = 'hoan_thanh'
        return True
