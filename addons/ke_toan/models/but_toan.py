# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ButToan(models.Model):
    """Bút toán kế toán"""
    _name = 'ke_toan.but_toan'
    _description = 'Bút toán kế toán'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'so_chung_tu'
    _order = 'ngay_chung_tu desc, id desc'

    so_chung_tu = fields.Char(string='Số chứng từ', required=True, copy=False, readonly=True,
                               default=lambda self: self.env['ir.sequence'].next_by_code('ke_toan.but_toan') or 'New')
    ngay_chung_tu = fields.Date(string='Ngày chứng từ', required=True, 
                                 default=fields.Date.context_today, tracking=True)
    
    loai_chung_tu = fields.Selection([
        ('thu', 'Phiếu thu'),
        ('chi', 'Phiếu chi'),
        ('nhap', 'Phiếu nhập'),
        ('xuat', 'Phiếu xuất'),
        ('khau_hao', 'Khấu hao tài sản'),
        ('luong', 'Chi phí lương'),
        ('mua_sam', 'Mua sắm tài sản'),
        ('thanh_ly', 'Thanh lý tài sản'),
        ('dieu_chinh', 'Điều chỉnh'),
        ('khac', 'Khác'),
    ], string='Loại chứng từ', required=True, default='khac', tracking=True)
    
    ky_ke_toan_id = fields.Many2one('ke_toan.ky', string='Kỳ kế toán',
                                     compute='_compute_ky_ke_toan', store=True)
    
    dien_giai = fields.Text(string='Diễn giải', required=True)
    
    # Chi tiết bút toán
    chi_tiet_ids = fields.One2many('ke_toan.but_toan_chi_tiet', 'but_toan_id', string='Chi tiết')
    
    # Tổng hợp
    tong_no = fields.Float(string='Tổng Nợ', compute='_compute_tong', store=True)
    tong_co = fields.Float(string='Tổng Có', compute='_compute_tong', store=True)
    chenh_lech = fields.Float(string='Chênh lệch', compute='_compute_tong', store=True)
    can_doi = fields.Boolean(string='Cân đối', compute='_compute_tong', store=True)
    
    # Liên kết module khác
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên liên quan')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản liên quan')
    bang_luong_id = fields.Many2one('bang_luong', string='Bảng lương liên quan')
    khau_hao_id = fields.Many2one('khau_hao', string='Khấu hao liên quan')
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_ghi_so', 'Đã ghi sổ'),
        ('huy', 'Đã hủy'),
    ], string='Trạng thái', default='nhap', required=True, tracking=True)
    
    nguoi_lap_id = fields.Many2one('res.users', string='Người lập', 
                                    default=lambda self: self.env.user, readonly=True)
    nguoi_duyet_id = fields.Many2one('res.users', string='Người duyệt')
    ngay_duyet = fields.Datetime(string='Ngày duyệt')
    
    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('ngay_chung_tu')
    def _compute_ky_ke_toan(self):
        for record in self:
            if record.ngay_chung_tu:
                ky = self.env['ke_toan.ky'].search([
                    ('ngay_bat_dau', '<=', record.ngay_chung_tu),
                    ('ngay_ket_thuc', '>=', record.ngay_chung_tu),
                    ('trang_thai', '!=', 'khoa'),
                ], limit=1)
                record.ky_ke_toan_id = ky.id if ky else False
            else:
                record.ky_ke_toan_id = False

    @api.depends('chi_tiet_ids.so_tien_no', 'chi_tiet_ids.so_tien_co')
    def _compute_tong(self):
        for record in self:
            record.tong_no = sum(record.chi_tiet_ids.mapped('so_tien_no'))
            record.tong_co = sum(record.chi_tiet_ids.mapped('so_tien_co'))
            record.chenh_lech = abs(record.tong_no - record.tong_co)
            record.can_doi = (record.chenh_lech < 0.01)  # Cho phép sai số nhỏ

    @api.model
    def create(self, vals):
        if vals.get('so_chung_tu', 'New') == 'New':
            vals['so_chung_tu'] = self.env['ir.sequence'].next_by_code('ke_toan.but_toan') or 'BT001'
        return super(ButToan, self).create(vals)

    def action_gui_duyet(self):
        """Gửi duyệt bút toán"""
        for record in self:
            if not record.chi_tiet_ids:
                raise ValidationError('Bút toán phải có ít nhất một dòng chi tiết!')
            if not record.can_doi:
                raise ValidationError(f'Bút toán không cân đối! Chênh lệch: {record.chenh_lech:,.0f}')
            record.trang_thai = 'cho_duyet'
        return True

    def action_duyet(self):
        """Duyệt và ghi sổ bút toán"""
        for record in self:
            if not record.can_doi:
                raise ValidationError('Bút toán không cân đối!')
            if record.ky_ke_toan_id and record.ky_ke_toan_id.trang_thai == 'khoa':
                raise ValidationError('Kỳ kế toán đã khóa, không thể ghi sổ!')
            record.write({
                'trang_thai': 'da_ghi_so',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
            })
        return True

    def action_huy(self):
        """Hủy bút toán"""
        for record in self:
            if record.trang_thai == 'da_ghi_so':
                if record.ky_ke_toan_id and record.ky_ke_toan_id.trang_thai == 'khoa':
                    raise ValidationError('Kỳ kế toán đã khóa, không thể hủy!')
            record.trang_thai = 'huy'
        return True

    def action_nhap_lai(self):
        """Đưa về trạng thái nháp"""
        for record in self:
            if record.trang_thai in ['cho_duyet', 'huy']:
                record.trang_thai = 'nhap'
        return True


class ButToanChiTiet(models.Model):
    """Chi tiết bút toán"""
    _name = 'ke_toan.but_toan_chi_tiet'
    _description = 'Chi tiết bút toán'
    _order = 'sequence, id'

    but_toan_id = fields.Many2one('ke_toan.but_toan', string='Bút toán', 
                                   required=True, ondelete='cascade')
    sequence = fields.Integer(string='Thứ tự', default=10)
    
    tai_khoan_id = fields.Many2one('ke_toan.tai_khoan', string='Tài khoản', required=True,
                                    domain=[('cho_phep_ghi_so', '=', True)])
    ma_tai_khoan = fields.Char(related='tai_khoan_id.ma_tai_khoan', string='Mã TK', store=True)
    
    dien_giai = fields.Char(string='Diễn giải')
    
    so_tien_no = fields.Float(string='Nợ', default=0.0)
    so_tien_co = fields.Float(string='Có', default=0.0)
    
    # Đối tượng liên quan
    doi_tuong_model = fields.Selection([
        ('nhan_vien', 'Nhân viên'),
        ('phong_ban', 'Phòng ban'),
        ('tai_san', 'Tài sản'),
        ('nha_cung_cap', 'Nhà cung cấp'),
        ('khach_hang', 'Khách hàng'),
    ], string='Loại đối tượng')
    doi_tuong_id = fields.Integer(string='ID đối tượng')
    doi_tuong_name = fields.Char(string='Tên đối tượng', compute='_compute_doi_tuong_name')

    @api.depends('doi_tuong_model', 'doi_tuong_id')
    def _compute_doi_tuong_name(self):
        for record in self:
            if record.doi_tuong_model and record.doi_tuong_id:
                try:
                    obj = self.env[record.doi_tuong_model].browse(record.doi_tuong_id)
                    record.doi_tuong_name = obj.display_name if obj.exists() else ''
                except:
                    record.doi_tuong_name = ''
            else:
                record.doi_tuong_name = ''

    @api.constrains('so_tien_no', 'so_tien_co')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien_no < 0 or record.so_tien_co < 0:
                raise ValidationError('Số tiền phải >= 0!')
            if record.so_tien_no == 0 and record.so_tien_co == 0:
                raise ValidationError('Phải nhập số tiền Nợ hoặc Có!')
