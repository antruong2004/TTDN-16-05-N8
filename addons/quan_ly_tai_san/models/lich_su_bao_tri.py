# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LichSuBaoTri(models.Model):
    _name = 'lich_su_bao_tri'
    _description = 'Lịch sử bảo trì tài sản'
    _order = 'ngay_bao_tri desc'

    ma_phieu = fields.Char(string='Mã phiếu', required=True, copy=False, readonly=True,
                          default=lambda self: self.env['ir.sequence'].next_by_code('lich_su_bao_tri') or 'New')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    ngay_bao_tri = fields.Date(string='Ngày bảo trì', required=True, default=fields.Date.context_today)
    loai_bao_tri = fields.Selection([
        ('dinh_ky', 'Bảo trì định kỳ'),
        ('sua_chua', 'Sửa chữa'),
        ('thay_the_linh_kien', 'Thay thế linh kiện'),
        ('nang_cap', 'Nâng cấp'),
        ('kiem_tra', 'Kiểm tra'),
    ], string='Loại bảo trì', required=True, default='dinh_ky')
    
    noi_dung = fields.Text(string='Nội dung bảo trì', required=True)
    nguoi_thuc_hien = fields.Char(string='Người thực hiện')
    don_vi_bao_tri = fields.Char(string='Đơn vị bảo trì')
    chi_phi = fields.Float(string='Chi phí', default=0.0)
    
    linh_kien_thay_the = fields.Text(string='Linh kiện thay thế')
    ket_qua = fields.Text(string='Kết quả')
    
    trang_thai = fields.Selection([
        ('ke_hoach', 'Kế hoạch'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Đã hủy'),
    ], string='Trạng thái', default='ke_hoach', required=True)
    
    ngay_hoan_thanh = fields.Date(string='Ngày hoàn thành')
    danh_gia = fields.Selection([
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('can_theo_doi', 'Cần theo dõi'),
    ], string='Đánh giá')
    
    ghi_chu = fields.Text(string='Ghi chú')
    file_dinh_kem_ids = fields.Many2many('ir.attachment', string='File đính kèm')

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('lich_su_bao_tri') or 'BT001'
        return super(LichSuBaoTri, self).create(vals)

    def action_bat_dau(self):
        """Bắt đầu bảo trì"""
        self.write({'trang_thai': 'dang_thuc_hien'})

    def action_hoan_thanh(self):
        """Hoàn thành bảo trì"""
        self.write({
            'trang_thai': 'hoan_thanh',
            'ngay_hoan_thanh': fields.Date.context_today(self)
        })
        # Cập nhật ngày bảo trì cuối cho tài sản
        if self.tai_san_id:
            self.tai_san_id.write({'lan_bao_tri_cuoi': self.ngay_bao_tri})
