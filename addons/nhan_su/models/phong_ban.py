<<<<<<< HEAD
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
=======
# -*- coding: utf-8 -*-
from odoo import models, fields, api
>>>>>>> cc63fe88 (update)


class PhongBan(models.Model):
    _name = 'phong_ban'
<<<<<<< HEAD
    _description = 'Phòng ban'
    _rec_name = 'ten_phong_ban'
    _order = 'ma_dinh_danh asc'
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất!'),
    ]

    ma_dinh_danh = fields.Char(
        string="Mã định danh",
        required=True,
        copy=False,
        index=True
    )

    ten_phong_ban = fields.Char(
        string="Tên phòng ban",
        required=True,
        index=True
    )
    
    truong_phong_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Trưởng phòng"
    )

    mo_ta = fields.Text(
        string="Mô tả"
    )

    nhan_vien_ids = fields.Many2many(
        comodel_name='nhan_vien',
        relation='phong_ban_nhan_vien_rel',
        column1='phong_ban_id',
        column2='nhan_vien_id',
        string='Danh sách nhân viên'
    )
    
    so_luong_nhan_vien = fields.Integer(
        string="Số lượng nhân viên",
        compute='_compute_so_luong_nhan_vien',
        store=True
    )
    
    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )

    @api.depends('nhan_vien_ids')
    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_nhan_vien = len(record.nhan_vien_ids)
=======
    _description = 'Phòng ban trong tổ chức'
    _rec_name = 'ten_phong_ban'
    _order = 'ma_phong_ban'

    ma_phong_ban = fields.Char(string='Mã phòng ban', required=True)
    ten_phong_ban = fields.Char(string='Tên phòng ban', required=True)
    mo_ta = fields.Text(string='Mô tả')
    truong_phong_id = fields.Many2one('nhan_vien', string='Trưởng phòng')
    phong_ban_cha_id = fields.Many2one('phong_ban', string='Phòng ban cha')
    phong_ban_con_ids = fields.One2many('phong_ban', 'phong_ban_cha_id', string='Phòng ban con')
    nhan_vien_ids = fields.One2many('nhan_vien', 'phong_ban_id', string='Danh sách nhân viên')
    so_nhan_vien = fields.Integer(string='Số nhân viên', compute='_compute_so_nhan_vien', store=True)
    active = fields.Boolean(string='Hoạt động', default=True)
    
    # Relationships - Liên kết với các models khác
    cham_cong_ids = fields.One2many('cham_cong', 'phong_ban_id', string='Chấm công phòng ban')
    bang_luong_ids = fields.One2many('bang_luong', 'phong_ban_id', string='Bảng lương phòng ban')
    
    # Computed fields - Thống kê
    tong_luong_thang_nay = fields.Float(string='Tổng lương tháng này', compute='_compute_thong_ke_phong_ban')
    so_nhan_vien_dang_lam = fields.Integer(string='Số NV đang làm', compute='_compute_thong_ke_phong_ban')
    
    @api.depends('nhan_vien_ids')
    def _compute_so_nhan_vien(self):
        for record in self:
            record.so_nhan_vien = len(record.nhan_vien_ids)
    
    @api.depends('bang_luong_ids', 'nhan_vien_ids')
    def _compute_thong_ke_phong_ban(self):
        """Tính toán thống kê cho phòng ban"""
        for record in self:
            today = fields.Date.today()
            thang = today.month
            nam = today.year
            
            # Tổng lương tháng này
            bang_luong_thang_nay = record.bang_luong_ids.filtered(
                lambda r: r.thang == thang and r.nam == nam
            )
            record.tong_luong_thang_nay = sum(bang_luong_thang_nay.mapped('thuc_linh'))
            
            # Số nhân viên đang làm việc
            record.so_nhan_vien_dang_lam = len(record.nhan_vien_ids.filtered(
                lambda r: r.trang_thai in ['chinh_thuc', 'thu_viec']
            ))
    
    _sql_constraints = [
        ('ma_phong_ban_unique', 'UNIQUE(ma_phong_ban)', 'Mã phòng ban phải là duy nhất!')
    ]
>>>>>>> cc63fe88 (update)
