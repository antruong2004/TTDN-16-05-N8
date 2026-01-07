# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Tài sản'
    _rec_name = 'ten_tai_san'
    _order = 'ma_tai_san asc'
    
    _sql_constraints = [
        ('ma_tai_san_unique', 'unique(ma_tai_san)', 'Mã tài sản phải là duy nhất!'),
    ]

    ma_tai_san = fields.Char(
        string="Mã tài sản",
        required=True,
        copy=False,
        index=True
    )
    
    ten_tai_san = fields.Char(
        string="Tên tài sản",
        required=True,
        index=True
    )
    
    loai_tai_san_id = fields.Many2one(
        comodel_name='loai_tai_san',
        string="Loại tài sản",
        required=True,
        ondelete='restrict'
    )
    
    ngay_mua = fields.Date(
        string="Ngày mua",
        required=True,
        default=fields.Date.context_today
    )
    
    ngay_bat_dau_khau_hao = fields.Date(
        string="Ngày bắt đầu khấu hao",
        required=True,
        default=fields.Date.context_today
    )
    
    nguyen_gia = fields.Float(
        string="Nguyên giá",
        required=True,
        digits=(16, 2),
        help="Giá trị ban đầu của tài sản"
    )
    
    gia_tri_con_lai = fields.Float(
        string="Giá trị còn lại",
        compute='_compute_gia_tri_con_lai',
        store=True,
        digits=(16, 2)
    )
    
    gia_tri_khau_hao_luy_ke = fields.Float(
        string="Giá trị khấu hao lũy kế",
        compute='_compute_gia_tri_khau_hao_luy_ke',
        store=True,
        digits=(16, 2)
    )
    
    thoi_gian_khau_hao = fields.Integer(
        related='loai_tai_san_id.thoi_gian_khau_hao',
        string="Thời gian khấu hao (tháng)",
        store=True
    )
    
    phuong_phap_khau_hao = fields.Selection(
        related='loai_tai_san_id.phuong_phap_khau_hao',
        string="Phương pháp khấu hao",
        store=True
    )
    
    khau_hao_hang_thang = fields.Float(
        string="Khấu hao hàng tháng",
        compute='_compute_khau_hao_hang_thang',
        store=True,
        digits=(16, 2)
    )
    
    trang_thai = fields.Selection(
        selection=[
            ('dang_su_dung', 'Đang sử dụng'),
            ('bao_tri', 'Bảo trì'),
            ('khau_hao_het', 'Khấu hao hết'),
            ('thanh_ly', 'Thanh lý'),
        ],
        string="Trạng thái",
        default='dang_su_dung',
        required=True
    )
    
    vi_tri = fields.Char(string="Vị trí")
    
    nguoi_quan_ly_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Người quản lý",
        ondelete='set null'
    )
    
    phong_ban_id = fields.Many2one(
        comodel_name='phong_ban',
        string="Phòng ban",
        ondelete='set null'
    )
    
    ghi_chu = fields.Text(string="Ghi chú")
    
    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )
    
    khau_hao_ids = fields.One2many(
        comodel_name='khau_hao',
        inverse_name='tai_san_id',
        string='Lịch sử khấu hao'
    )
    
    so_thang_da_khau_hao = fields.Integer(
        string="Số tháng đã khấu hao",
        compute='_compute_so_thang_da_khau_hao',
        store=True
    )

    @api.depends('loai_tai_san_id.thoi_gian_khau_hao', 'nguyen_gia', 'phuong_phap_khau_hao', 'gia_tri_con_lai', 'loai_tai_san_id.he_so_khau_hao')
    def _compute_khau_hao_hang_thang(self):
        for record in self:
            if record.thoi_gian_khau_hao <= 0:
                record.khau_hao_hang_thang = 0.0
                continue
                
            if record.phuong_phap_khau_hao == 'duong_thang':
                # Khấu hao đường thẳng: chia đều
                record.khau_hao_hang_thang = record.nguyen_gia / record.thoi_gian_khau_hao
            elif record.phuong_phap_khau_hao == 'so_du_giam_dan':
                # Khấu hao số dư giảm dần: tính theo giá trị còn lại
                ty_le_khau_hao_thang = (1.0 / record.thoi_gian_khau_hao) * (record.loai_tai_san_id.he_so_khau_hao or 2.0)
                record.khau_hao_hang_thang = record.gia_tri_con_lai * ty_le_khau_hao_thang
            else:
                record.khau_hao_hang_thang = 0.0

    @api.depends('khau_hao_ids.gia_tri_khau_hao')
    def _compute_gia_tri_khau_hao_luy_ke(self):
        for record in self:
            record.gia_tri_khau_hao_luy_ke = sum(record.khau_hao_ids.mapped('gia_tri_khau_hao'))

    @api.depends('nguyen_gia', 'gia_tri_khau_hao_luy_ke')
    def _compute_gia_tri_con_lai(self):
        for record in self:
            record.gia_tri_con_lai = record.nguyen_gia - record.gia_tri_khau_hao_luy_ke

    @api.depends('khau_hao_ids')
    def _compute_so_thang_da_khau_hao(self):
        for record in self:
            record.so_thang_da_khau_hao = len(record.khau_hao_ids)

    @api.constrains('nguyen_gia')
    def _check_nguyen_gia(self):
        for record in self:
            if record.nguyen_gia <= 0:
                raise ValidationError(_('Nguyên giá phải lớn hơn 0!'))

    @api.constrains('ngay_bat_dau_khau_hao', 'ngay_mua')
    def _check_ngay_khau_hao(self):
        for record in self:
            if record.ngay_bat_dau_khau_hao < record.ngay_mua:
                raise ValidationError(_('Ngày bắt đầu khấu hao không thể trước ngày mua!'))

    def action_tao_khau_hao_tu_dong(self):
        """Tạo khấu hao tự động cho tài sản"""
        self.ensure_one()
        
        if self.trang_thai not in ['dang_su_dung', 'bao_tri']:
            raise ValidationError(_('Chỉ có thể tạo khấu hao cho tài sản đang sử dụng hoặc bảo trì!'))
        
        # Tính tháng hiện tại
        ngay_hien_tai = date.today()
        thang_hien_tai = ngay_hien_tai.replace(day=1)
        
        # Kiểm tra đã có khấu hao tháng này chưa
        khau_hao_da_co = self.env['khau_hao'].search([
            ('tai_san_id', '=', self.id),
            ('thang', '=', thang_hien_tai.month),
            ('nam', '=', thang_hien_tai.year)
        ])
        
        if khau_hao_da_co:
            raise ValidationError(_('Đã có khấu hao cho tháng này!'))
        
        # Kiểm tra còn khấu hao không
        if self.so_thang_da_khau_hao >= self.thoi_gian_khau_hao:
            raise ValidationError(_('Tài sản đã khấu hao hết!'))
        
        # Tạo bản ghi khấu hao
        self.env['khau_hao'].create({
            'tai_san_id': self.id,
            'thang': thang_hien_tai.month,
            'nam': thang_hien_tai.year,
            'gia_tri_khau_hao': self.khau_hao_hang_thang,
        })
        
        # Cập nhật trạng thái nếu khấu hao hết
        if self.so_thang_da_khau_hao + 1 >= self.thoi_gian_khau_hao:
            self.trang_thai = 'khau_hao_het'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Thành công'),
                'message': _('Đã tạo khấu hao cho tháng %s/%s') % (thang_hien_tai.month, thang_hien_tai.year),
                'type': 'success',
                'sticky': False,
            }
        }
