# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SoCai(models.Model):
    _name = 'so_cai'
    _description = 'Sổ cái kế toán'
    _rec_name = 'ma_chung_tu'
    _order = 'ngay_ghi_so desc, id desc'

    ma_chung_tu = fields.Char(
        string="Mã chứng từ",
        required=True,
        copy=False,
        index=True
    )
    
    ngay_ghi_so = fields.Date(
        string="Ngày ghi sổ",
        required=True,
        default=fields.Date.context_today,
        index=True
    )
    
    dien_giai = fields.Char(
        string="Diễn giải",
        required=True
    )
    
    tai_khoan_no_id = fields.Many2one(
        comodel_name='tai_khoan_ke_toan',
        string="TK Nợ",
        required=True,
        ondelete='restrict'
    )
    
    tai_khoan_co_id = fields.Many2one(
        comodel_name='tai_khoan_ke_toan',
        string="TK Có",
        required=True,
        ondelete='restrict'
    )
    
    so_tien = fields.Float(
        string="Số tiền",
        required=True,
        digits=(16, 2)
    )
    
    loai_chung_tu = fields.Selection(
        selection=[
            ('khau_hao', 'Khấu hao'),
            ('thu', 'Thu'),
            ('chi', 'Chi'),
            ('chuyen_khoan', 'Chuyển khoản'),
            ('dieu_chinh', 'Điều chỉnh'),
            ('khac', 'Khác'),
        ],
        string="Loại chứng từ",
        default='khac',
        required=True
    )
    
    trang_thai = fields.Selection(
        selection=[
            ('nhap', 'Nhập'),
            ('da_ghi_so', 'Đã ghi sổ'),
            ('da_khoa_so', 'Đã khóa sổ'),
        ],
        string="Trạng thái",
        default='nhap',
        required=True
    )
    
    ghi_chu = fields.Text(string="Ghi chú")
    
    # Liên kết với Nhân sự
    nguoi_lap_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Người lập",
        default=lambda self: self.env.user.employee_id if hasattr(self.env.user, 'employee_id') else False,
        ondelete='set null'
    )
    
    nguoi_duyet_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Người duyệt",
        ondelete='set null'
    )
    
    phong_ban_id = fields.Many2one(
        comodel_name='phong_ban',
        string="Phòng ban",
        ondelete='set null',
        help="Phòng ban liên quan đến chứng từ"
    )
    
    # Liên kết ngược với khấu hao
    khau_hao_ids = fields.One2many(
        comodel_name='khau_hao',
        inverse_name='so_cai_id',
        string='Khấu hao liên quan'
    )

    @api.constrains('so_tien')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien <= 0:
                raise ValidationError(_('Số tiền phải lớn hơn 0!'))

    @api.constrains('tai_khoan_no_id', 'tai_khoan_co_id')
    def _check_tai_khoan(self):
        for record in self:
            if record.tai_khoan_no_id == record.tai_khoan_co_id:
                raise ValidationError(_('Tài khoản Nợ và Có không thể giống nhau!'))

    def action_ghi_so(self):
        """Ghi sổ chứng từ"""
        for record in self:
            if record.trang_thai == 'nhap':
                # Tự động gán người duyệt là user hiện tại
                if not record.nguoi_duyet_id and self.env.user.employee_id:
                    record.nguoi_duyet_id = self.env.user.employee_id
                record.trang_thai = 'da_ghi_so'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': _('Đã ghi sổ chứng từ'),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_khoa_so(self):
        """Khóa sổ chứng từ"""
        for record in self:
            if record.trang_thai == 'da_ghi_so':
                record.trang_thai = 'da_khoa_so'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': _('Đã khóa sổ chứng từ'),
                'type': 'success',
                'sticky': False,
            }
        }
