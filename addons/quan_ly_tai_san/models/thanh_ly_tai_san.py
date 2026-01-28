# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ThanhLyTaiSan(models.Model):
    _name = 'thanh_ly_tai_san'
    _description = 'Thanh lý tài sản'
    _rec_name = 'ma_phieu'

    ma_phieu = fields.Char(string='Mã phiếu', required=True, copy=False, readonly=True,
                          default=lambda self: self.env['ir.sequence'].next_by_code('thanh_ly_tai_san') or 'New')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True)
    ngay_thanh_ly = fields.Date(string='Ngày thanh lý', required=True, default=fields.Date.context_today)
    ly_do = fields.Selection([
        ('hong', 'Hỏng hóc không sử dụng được'),
        ('cu', 'Hết thời gian sử dụng'),
        ('thay_the', 'Thay thế bằng tài sản mới'),
        ('khac', 'Lý do khác'),
    ], string='Lý do thanh lý', required=True)
    mo_ta_ly_do = fields.Text(string='Mô tả chi tiết')
    gia_tri_con_lai = fields.Float(string='Giá trị còn lại', related='tai_san_id.gia_tri_con_lai')
    gia_tri_thu_hoi = fields.Float(string='Giá trị thu hồi', default=0.0,
                                    help='Giá trị thu hồi từ bán phế liệu, thanh lý')
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
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('thanh_ly_tai_san') or 'TL001'
        return super(ThanhLyTaiSan, self).create(vals)

    def action_gui_duyet(self):
        """Gửi phiếu thanh lý để duyệt"""
        for record in self:
            if record.trang_thai == 'nhap':
                record.trang_thai = 'cho_duyet'
        return True

    def action_duyet(self):
        """Duyệt phiếu thanh lý"""
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({
                    'trang_thai': 'da_duyet',
                    'nguoi_duyet_id': self.env.user.id if hasattr(self.env.user, 'nhan_vien_id') else False,
                    'ngay_duyet': fields.Date.context_today(self)
                })
        return True

    def action_tu_choi(self):
        """Từ chối phiếu thanh lý"""
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
        """Hoàn thành thanh lý - cập nhật trạng thái tài sản"""
        for record in self:
            if record.trang_thai == 'da_duyet':
                record.tai_san_id.write({
                    'trang_thai': 'thanh_ly',
                    'active': False
                })
                record.trang_thai = 'hoan_thanh'
                
                # Hook: Tạo bút toán thanh lý nếu module kế toán đã cài
                if hasattr(record, 'action_tao_but_toan_thanh_ly'):
                    record.action_tao_but_toan_thanh_ly()
        return True
