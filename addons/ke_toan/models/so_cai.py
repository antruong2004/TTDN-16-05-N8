# -*- coding: utf-8 -*-

<<<<<<< HEAD
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
=======
from odoo import models, fields, api


class SoCai(models.Model):
    """Sổ cái kế toán - tổng hợp theo tài khoản"""
    _name = 'ke_toan.so_cai'
    _description = 'Sổ cái kế toán'
    _rec_name = 'tai_khoan_id'
    _order = 'ky_ke_toan_id desc, tai_khoan_id'

    tai_khoan_id = fields.Many2one('ke_toan.tai_khoan', string='Tài khoản', required=True, ondelete='cascade')
    ky_ke_toan_id = fields.Many2one('ke_toan.ky', string='Kỳ kế toán', required=True, ondelete='cascade')
    
    # Số dư đầu kỳ
    so_du_dau_ky_no = fields.Float(string='Dư đầu kỳ Nợ', default=0.0)
    so_du_dau_ky_co = fields.Float(string='Dư đầu kỳ Có', default=0.0)
    
    # Phát sinh trong kỳ
    phat_sinh_no = fields.Float(string='Phát sinh Nợ', compute='_compute_phat_sinh', store=True)
    phat_sinh_co = fields.Float(string='Phát sinh Có', compute='_compute_phat_sinh', store=True)
    
    # Số dư cuối kỳ
    so_du_cuoi_ky_no = fields.Float(string='Dư cuối kỳ Nợ', compute='_compute_so_du_cuoi_ky', store=True)
    so_du_cuoi_ky_co = fields.Float(string='Dư cuối kỳ Có', compute='_compute_so_du_cuoi_ky', store=True)
    
    # Liên kết bút toán
    but_toan_chi_tiet_ids = fields.One2many(
        'ke_toan.but_toan_chi_tiet',
        compute='_compute_but_toan_chi_tiet',
        string='Chi tiết bút toán'
    )

    @api.depends('tai_khoan_id', 'ky_ke_toan_id')
    def _compute_but_toan_chi_tiet(self):
        for record in self:
            if record.tai_khoan_id and record.ky_ke_toan_id:
                record.but_toan_chi_tiet_ids = self.env['ke_toan.but_toan_chi_tiet'].search([
                    ('tai_khoan_id', '=', record.tai_khoan_id.id),
                    ('but_toan_id.ky_ke_toan_id', '=', record.ky_ke_toan_id.id),
                    ('but_toan_id.trang_thai', '=', 'da_ghi_so'),
                ])
            else:
                record.but_toan_chi_tiet_ids = False

    @api.depends('but_toan_chi_tiet_ids.so_tien_no', 'but_toan_chi_tiet_ids.so_tien_co')
    def _compute_phat_sinh(self):
        for record in self:
            record.phat_sinh_no = sum(record.but_toan_chi_tiet_ids.mapped('so_tien_no'))
            record.phat_sinh_co = sum(record.but_toan_chi_tiet_ids.mapped('so_tien_co'))

    @api.depends('so_du_dau_ky_no', 'so_du_dau_ky_co', 'phat_sinh_no', 'phat_sinh_co')
    def _compute_so_du_cuoi_ky(self):
        for record in self:
            du_no = record.so_du_dau_ky_no + record.phat_sinh_no - record.phat_sinh_co
            du_co = record.so_du_dau_ky_co + record.phat_sinh_co - record.phat_sinh_no
            
            if du_no >= 0:
                record.so_du_cuoi_ky_no = du_no
                record.so_du_cuoi_ky_co = 0
            else:
                record.so_du_cuoi_ky_no = 0
                record.so_du_cuoi_ky_co = abs(du_no)

    _sql_constraints = [
        ('tai_khoan_ky_unique', 'unique(tai_khoan_id, ky_ke_toan_id)', 
         'Mỗi tài khoản chỉ có một dòng sổ cái trong một kỳ!')
    ]

    @api.model
    def tao_so_cai_ky(self, ky_ke_toan_id):
        """Tạo sổ cái cho tất cả tài khoản trong kỳ"""
        ky = self.env['ke_toan.ky'].browse(ky_ke_toan_id)
        tai_khoan_list = self.env['ke_toan.tai_khoan'].search([
            ('cho_phep_ghi_so', '=', True),
            ('active', '=', True),
        ])
        
        for tk in tai_khoan_list:
            existing = self.search([
                ('tai_khoan_id', '=', tk.id),
                ('ky_ke_toan_id', '=', ky.id),
            ], limit=1)
            if not existing:
                # Lấy số dư cuối kỳ trước
                ky_truoc = self.env['ke_toan.ky'].search([
                    ('ngay_ket_thuc', '<', ky.ngay_bat_dau),
                ], order='ngay_ket_thuc desc', limit=1)
                
                so_du_dau_no = 0.0
                so_du_dau_co = 0.0
                if ky_truoc:
                    so_cai_truoc = self.search([
                        ('tai_khoan_id', '=', tk.id),
                        ('ky_ke_toan_id', '=', ky_truoc.id),
                    ], limit=1)
                    if so_cai_truoc:
                        so_du_dau_no = so_cai_truoc.so_du_cuoi_ky_no
                        so_du_dau_co = so_cai_truoc.so_du_cuoi_ky_co
                
                self.create({
                    'tai_khoan_id': tk.id,
                    'ky_ke_toan_id': ky.id,
                    'so_du_dau_ky_no': so_du_dau_no,
                    'so_du_dau_ky_co': so_du_dau_co,
                })
        return True
>>>>>>> cc63fe88 (update)
