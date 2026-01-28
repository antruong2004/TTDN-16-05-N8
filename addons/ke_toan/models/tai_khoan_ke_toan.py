# -*- coding: utf-8 -*-

<<<<<<< HEAD
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class TaiKhoanKeToan(models.Model):
    _name = 'tai_khoan_ke_toan'
    _description = 'Tài khoản kế toán'
    _rec_name = 'ten_tai_khoan_day_du'
    _order = 'ma_tai_khoan asc'
    
    _sql_constraints = [
        ('ma_tai_khoan_unique', 'unique(ma_tai_khoan)', 'Mã tài khoản phải là duy nhất!'),
    ]

    ma_tai_khoan = fields.Char(
        string="Mã tài khoản",
        required=True,
        copy=False,
        index=True
    )
    
    ten_tai_khoan = fields.Char(
        string="Tên tài khoản",
        required=True,
        index=True
    )
    
    ten_tai_khoan_day_du = fields.Char(
        string="Tên đầy đủ",
        compute='_compute_ten_day_du',
        store=True
    )
    
    loai_tai_khoan = fields.Selection(
        selection=[
            ('tai_san', 'Tài sản'),
            ('nguon_von', 'Nguồn vốn'),
            ('doanh_thu', 'Doanh thu'),
            ('chi_phi', 'Chi phí'),
        ],
        string="Loại tài khoản",
        required=True
    )
    
    cap_do = fields.Integer(
        string="Cấp độ",
        compute='_compute_cap_do',
        store=True,
        help="Cấp độ của tài khoản dựa trên số ký tự mã"
    )
    
    tai_khoan_cha_id = fields.Many2one(
        comodel_name='tai_khoan_ke_toan',
        string="Tài khoản cha",
        ondelete='restrict',
        domain="[('cap_do', '<', cap_do)]"
    )
    
    tai_khoan_con_ids = fields.One2many(
        comodel_name='tai_khoan_ke_toan',
        inverse_name='tai_khoan_cha_id',
        string='Tài khoản con'
    )
    
    tinh_chat = fields.Selection(
        selection=[
            ('no', 'Nợ'),
            ('co', 'Có'),
            ('song_phia', 'Song phía'),
        ],
        string="Tính chất",
        required=True,
        help="Tính chất dư của tài khoản"
    )
    
    mo_ta = fields.Text(string="Mô tả")
    
    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )
    
    so_cai_no_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='tai_khoan_no_id',
        string='Sổ cái bên Nợ'
    )
    
    so_cai_co_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='tai_khoan_co_id',
        string='Sổ cái bên Có'
    )
    
    tong_no = fields.Float(
        string="Tổng Nợ",
        compute='_compute_tong_no_co',
        digits=(16, 2)
    )
    
    tong_co = fields.Float(
        string="Tổng Có",
        compute='_compute_tong_no_co',
        digits=(16, 2)
    )
    
    so_du = fields.Float(
        string="Số dư",
        compute='_compute_so_du',
        digits=(16, 2)
    )

    @api.depends('ma_tai_khoan', 'ten_tai_khoan')
    def _compute_ten_day_du(self):
        for record in self:
            if record.ma_tai_khoan and record.ten_tai_khoan:
                record.ten_tai_khoan_day_du = f"[{record.ma_tai_khoan}] {record.ten_tai_khoan}"
            elif record.ten_tai_khoan:
                record.ten_tai_khoan_day_du = record.ten_tai_khoan
            else:
                record.ten_tai_khoan_day_du = ""

    @api.depends('ma_tai_khoan')
    def _compute_cap_do(self):
        for record in self:
            if record.ma_tai_khoan:
                record.cap_do = len(record.ma_tai_khoan)
            else:
                record.cap_do = 0

    @api.depends('so_cai_no_ids.so_tien', 'so_cai_co_ids.so_tien')
    def _compute_tong_no_co(self):
        for record in self:
            record.tong_no = sum(record.so_cai_no_ids.mapped('so_tien'))
            record.tong_co = sum(record.so_cai_co_ids.mapped('so_tien'))

    @api.depends('tong_no', 'tong_co', 'tinh_chat')
    def _compute_so_du(self):
        for record in self:
            if record.tinh_chat == 'no':
                record.so_du = record.tong_no - record.tong_co
            elif record.tinh_chat == 'co':
                record.so_du = record.tong_co - record.tong_no
            else:  # song_phia
                record.so_du = record.tong_no - record.tong_co

    @api.constrains('ma_tai_khoan')
    def _check_ma_tai_khoan(self):
        for record in self:
            if not re.match(r'^\d+$', record.ma_tai_khoan):
                raise ValidationError(_('Mã tài khoản chỉ được chứa số!'))

    @api.constrains('tai_khoan_cha_id')
    def _check_tai_khoan_cha(self):
        for record in self:
            if record.tai_khoan_cha_id:
                # Kiểm tra mã tài khoản con phải bắt đầu bằng mã tài khoản cha
                if not record.ma_tai_khoan.startswith(record.tai_khoan_cha_id.ma_tai_khoan):
                    raise ValidationError(_(
                        'Mã tài khoản con phải bắt đầu bằng mã tài khoản cha!'
                    ))
=======
from odoo import models, fields, api


class TaiKhoanKeToan(models.Model):
    """Hệ thống tài khoản kế toán theo chuẩn Việt Nam"""
    _name = 'ke_toan.tai_khoan'
    _description = 'Tài khoản kế toán'
    _rec_name = 'display_name'
    _order = 'ma_tai_khoan'
    _parent_name = 'parent_id'
    _parent_store = True

    ma_tai_khoan = fields.Char(string='Mã tài khoản', required=True, copy=False, index=True)
    ten_tai_khoan = fields.Char(string='Tên tài khoản', required=True)
    display_name = fields.Char(string='Tên hiển thị', compute='_compute_display_name', store=True)
    
    loai_tai_khoan = fields.Selection([
        ('tai_san', 'Tài sản'),
        ('no_phai_tra', 'Nợ phải trả'),
        ('von_chu_so_huu', 'Vốn chủ sở hữu'),
        ('doanh_thu', 'Doanh thu'),
        ('chi_phi', 'Chi phí'),
    ], string='Loại tài khoản', required=True)
    
    nhom_tai_khoan = fields.Selection([
        # Loại 1: Tài sản
        ('tien', 'Tiền và tương đương tiền'),
        ('phai_thu', 'Phải thu'),
        ('hang_ton_kho', 'Hàng tồn kho'),
        ('tai_san_co_dinh', 'Tài sản cố định'),
        ('tai_san_khac', 'Tài sản khác'),
        # Loại 2: Nợ phải trả
        ('phai_tra', 'Phải trả'),
        ('vay', 'Vay và nợ thuê tài chính'),
        # Loại 3: Vốn chủ sở hữu
        ('von', 'Vốn và quỹ'),
        # Loại 4: Doanh thu
        ('doanh_thu_ban_hang', 'Doanh thu bán hàng'),
        ('doanh_thu_tai_chinh', 'Doanh thu tài chính'),
        ('doanh_thu_khac', 'Doanh thu khác'),
        # Loại 5: Chi phí
        ('gia_von', 'Giá vốn hàng bán'),
        ('chi_phi_ban_hang', 'Chi phí bán hàng'),
        ('chi_phi_quan_ly', 'Chi phí quản lý'),
        ('chi_phi_tai_chinh', 'Chi phí tài chính'),
        ('chi_phi_khac', 'Chi phí khác'),
        ('chi_phi_nhan_su', 'Chi phí nhân sự'),
        ('chi_phi_khau_hao', 'Chi phí khấu hao'),
    ], string='Nhóm tài khoản')
    
    tinh_chat = fields.Selection([
        ('no', 'Dư Nợ'),
        ('co', 'Dư Có'),
        ('luong_tinh', 'Lưỡng tính'),
    ], string='Tính chất', default='no', required=True)
    
    # Phân cấp tài khoản
    parent_id = fields.Many2one('ke_toan.tai_khoan', string='Tài khoản cha', ondelete='restrict')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('ke_toan.tai_khoan', 'parent_id', string='Tài khoản con')
    cap_tai_khoan = fields.Integer(string='Cấp tài khoản', compute='_compute_cap_tai_khoan', store=True)
    
    # Cờ đánh dấu
    la_tai_khoan_tong_hop = fields.Boolean(string='Là TK tổng hợp', default=False,
                                            help='Tài khoản tổng hợp không được ghi nhận trực tiếp')
    cho_phep_ghi_so = fields.Boolean(string='Cho phép ghi sổ', default=True)
    active = fields.Boolean(string='Đang sử dụng', default=True)
    
    # Thống kê
    so_du_no = fields.Float(string='Số dư Nợ', compute='_compute_so_du', store=True)
    so_du_co = fields.Float(string='Số dư Có', compute='_compute_so_du', store=True)
    but_toan_ids = fields.One2many('ke_toan.but_toan_chi_tiet', 'tai_khoan_id', string='Bút toán')
    
    mo_ta = fields.Text(string='Mô tả')

    @api.depends('ma_tai_khoan', 'ten_tai_khoan')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.ma_tai_khoan} - {record.ten_tai_khoan}"

    @api.depends('ma_tai_khoan')
    def _compute_cap_tai_khoan(self):
        for record in self:
            record.cap_tai_khoan = len(record.ma_tai_khoan) if record.ma_tai_khoan else 0

    @api.depends('but_toan_ids.so_tien_no', 'but_toan_ids.so_tien_co')
    def _compute_so_du(self):
        for record in self:
            tong_no = sum(record.but_toan_ids.filtered(
                lambda b: b.but_toan_id.trang_thai == 'da_ghi_so'
            ).mapped('so_tien_no'))
            tong_co = sum(record.but_toan_ids.filtered(
                lambda b: b.but_toan_id.trang_thai == 'da_ghi_so'
            ).mapped('so_tien_co'))
            record.so_du_no = tong_no
            record.so_du_co = tong_co

    _sql_constraints = [
        ('ma_tai_khoan_unique', 'unique(ma_tai_khoan)', 'Mã tài khoản phải duy nhất!')
    ]
>>>>>>> cc63fe88 (update)
