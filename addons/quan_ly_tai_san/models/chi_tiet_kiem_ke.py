# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ChiTietKiemKe(models.Model):
    _name = 'chi_tiet_kiem_ke'
    _description = 'Chi tiết kiểm kê'

    kiem_ke_id = fields.Many2one('kiem_ke_tai_san', string='Kiểm kê', required=True, ondelete='cascade')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True)
    so_luong_so_sach = fields.Integer(string='Số lượng sổ sách', default=1)
    so_luong_thuc_te = fields.Integer(string='Số lượng thực tế', default=1)
    chenh_lech = fields.Integer(string='Chênh lệch', compute='_compute_chenh_lech', store=True)
    tinh_trang = fields.Selection([
        ('tot', 'Tốt'),
        ('trung_binh', 'Trung bình'),
        ('kem', 'Kém'),
        ('hong', 'Hỏng'),
    ], string='Tình trạng', default='tot')
    vi_tri_thuc_te = fields.Char(string='Vị trí thực tế')
    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('so_luong_so_sach', 'so_luong_thuc_te')
    def _compute_chenh_lech(self):
        for record in self:
            record.chenh_lech = record.so_luong_thuc_te - record.so_luong_so_sach
