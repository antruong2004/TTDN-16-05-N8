# -*- coding: utf-8 -*-
<<<<<<< HEAD

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
=======
from odoo import models, fields, api
>>>>>>> cc63fe88 (update)


class ChucVu(models.Model):
    _name = 'chuc_vu'
<<<<<<< HEAD
    _description = 'Chức vụ'
    _rec_name = 'ten_chuc_vu'
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

    ten_chuc_vu = fields.Char(
        string="Tên chức vụ",
        required=True,
        index=True
    )
    
    cap_bac = fields.Selection(
        selection=[
            ('nhan_vien', 'Nhân viên'),
            ('truong_nhom', 'Trưởng nhóm'),
            ('truong_phong', 'Trưởng phòng'),
            ('pho_giam_doc', 'Phó giám đốc'),
            ('giam_doc', 'Giám đốc'),
        ],
        string="Cấp bậc"
    )

    mo_ta = fields.Text(
        string="Mô tả"
    )

    luong_co_ban = fields.Float(
        string="Lương cơ bản",
        digits=(16, 0)
    )

    phong_ban_id = fields.Many2one(
        comodel_name='phong_ban',
        string="Phòng ban"
    )

    nhan_vien_ids = fields.One2many(
        comodel_name='nhan_vien',
        inverse_name='chuc_vu_id',
        string='Nhân viên'
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

    @api.constrains('luong_co_ban')
    def _check_luong_co_ban(self):
        for record in self:
            if record.luong_co_ban and record.luong_co_ban < 0:
                raise ValidationError('Lương cơ bản phải lớn hơn 0!')
=======
    _description = 'Chức vụ trong tổ chức'
    _rec_name = 'ten_chuc_vu'
    _order = 'cap_bac desc, ma_chuc_vu'

    ma_chuc_vu = fields.Char(string='Mã chức vụ', required=True)
    ten_chuc_vu = fields.Char(string='Tên chức vụ', required=True)
    mo_ta = fields.Text(string='Mô tả')
    cap_bac = fields.Integer(string='Cấp bậc', default=1, help='Cấp bậc càng cao thì chức vụ càng lớn')
    luong_co_ban = fields.Float(string='Lương cơ bản')
    phu_cap = fields.Float(string='Phụ cấp chức vụ')
    nhan_vien_ids = fields.One2many('nhan_vien', 'chuc_vu_id', string='Danh sách nhân viên')
    so_nhan_vien = fields.Integer(string='Số nhân viên', compute='_compute_so_nhan_vien')
    active = fields.Boolean(string='Hoạt động', default=True)
    
    # Relationships - Liên kết với các models khác
    bang_luong_ids = fields.One2many('bang_luong', 'chuc_vu_id', string='Bảng lương theo chức vụ')
    
    # Computed fields - Thống kê
    trung_binh_luong_thuc_linh = fields.Float(string='TB lương thực lĩnh', compute='_compute_thong_ke_chuc_vu')
    
    @api.depends('nhan_vien_ids')
    def _compute_so_nhan_vien(self):
        for record in self:
            record.so_nhan_vien = len(record.nhan_vien_ids)
    
    @api.depends('bang_luong_ids')
    def _compute_thong_ke_chuc_vu(self):
        """Tính toán thống kê cho chức vụ"""
        for record in self:
            today = fields.Date.today()
            thang = today.month
            nam = today.year
            
            # Trung bình lương thực lĩnh tháng này
            bang_luong_thang_nay = record.bang_luong_ids.filtered(
                lambda r: r.thang == thang and r.nam == nam
            )
            if bang_luong_thang_nay:
                record.trung_binh_luong_thuc_linh = sum(bang_luong_thang_nay.mapped('thuc_linh')) / len(bang_luong_thang_nay)
            else:
                record.trung_binh_luong_thuc_linh = 0
    
    _sql_constraints = [
        ('ma_chuc_vu_unique', 'UNIQUE(ma_chuc_vu)', 'Mã chức vụ phải là duy nhất!')
    ]
>>>>>>> cc63fe88 (update)
