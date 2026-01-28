# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PhanBoTaiSan(models.Model):
    _name = 'phan_bo_tai_san'
    _description = 'Phân bổ tài sản'
    _rec_name = 'tai_san_id'

    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên')
    ngay_phan_bo = fields.Date(string='Ngày phân bổ', required=True, default=fields.Date.context_today)
    ngay_thu_hoi = fields.Date(string='Ngày thu hồi')
    ly_do = fields.Text(string='Lý do phân bổ')
    trang_thai = fields.Selection([
        ('dang_su_dung', 'Đang sử dụng'),
        ('da_thu_hoi', 'Đã thu hồi'),
    ], string='Trạng thái', default='dang_su_dung', required=True)
    ghi_chu = fields.Text(string='Ghi chú')

    @api.model
    def create(self, vals):
        result = super(PhanBoTaiSan, self).create(vals)
        # Cập nhật thông tin phòng ban và người quản lý cho tài sản
        if result.tai_san_id:
            result.tai_san_id.write({
                'phong_ban_id': result.phong_ban_id.id,
                'nguoi_quan_ly_id': result.nhan_vien_id.id if result.nhan_vien_id else False,
                'trang_thai': 'dang_su_dung'
            })
        return result
