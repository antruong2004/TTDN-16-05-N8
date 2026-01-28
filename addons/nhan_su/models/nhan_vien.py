# -*- coding: utf-8 -*-
<<<<<<< HEAD

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import re
=======
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
>>>>>>> cc63fe88 (update)


class NhanVien(models.Model):
    _name = 'nhan_vien'
<<<<<<< HEAD
    _description = 'Bảng chứa thông tin nhân viên'
    _order = 'ma_dinh_danh asc'
    _rec_name = 'name'

    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất!'),
        ('email_unique', 'unique(email)', 'Email đã được sử dụng!'),
    ]

    ma_dinh_danh = fields.Char(
        string="Mã định danh",
        required=True,
        copy=False,
        index=True
    )

    ho_ten = fields.Char(
        string="Họ và tên",
        required=True,
        index=True
    )

    name = fields.Char(
        string="Tên hiển thị",
        compute='_compute_name',
        store=True
    )

    ngay_sinh = fields.Date(string="Ngày sinh")

    tuoi = fields.Integer(
        string="Tuổi",
        compute='_compute_tuoi',
        store=True
    )

    gioi_tinh = fields.Selection(
        selection=[
            ('nam', 'Nam'),
            ('nu', 'Nữ'),
            ('khac', 'Khác'),
        ],
        string="Giới tính"
    )

    que_quan = fields.Char(string="Quê quán")
    dia_chi = fields.Char(string="Địa chỉ")

    email = fields.Char(
        string="Email",
        index=True
    )

    so_dien_thoai = fields.Char(string="Số điện thoại")

    so_bhxh = fields.Char(
        string="Số BHXH",
        copy=False
    )

    luong = fields.Float(
        string="Lương",
        digits=(16, 0)
    )

    active = fields.Boolean(
        string="Hoạt động",
        default=True
    )

    chuc_vu_id = fields.Many2one(
        comodel_name='chuc_vu',
        string="Chức vụ"
    )

    phong_ban_ids = fields.Many2many(
        comodel_name='phong_ban',
        relation='phong_ban_nhan_vien_rel',
        column1='nhan_vien_id',
        column2='phong_ban_id',
        string='Phòng ban'
    )

    lich_su_cong_tac_ids = fields.One2many(
        comodel_name='lich_su_cong_tac',
        inverse_name='nhan_vien_id',
        string='Lịch sử công tác'
    )

    chung_chi_ids = fields.One2many(
        comodel_name='chung_chi',
        inverse_name='nhan_vien_id',
        string='Chứng chỉ'
    )

    cham_cong_ids = fields.One2many(
        comodel_name='cham_cong',
        inverse_name='nhan_vien_id',
        string='Chấm công'
    )

    bang_luong_ids = fields.One2many(
        comodel_name='bang_luong',
        inverse_name='nhan_vien_id',
        string='Bảng lương'
    )

    # ================= COMPUTE =================

    @api.depends('ho_ten', 'ma_dinh_danh')
    def _compute_name(self):
        for record in self:
            if record.ho_ten and record.ma_dinh_danh:
                record.name = f"[{record.ma_dinh_danh}] {record.ho_ten}"
            elif record.ho_ten:
                record.name = record.ho_ten
            else:
                record.name = record.ma_dinh_danh or ''

=======
    _description = 'Thông tin nhân viên'
    _rec_name = 'ho_ten'
    _order = 'ma_dinh_danh'

    # Thông tin cơ bản
    ma_dinh_danh = fields.Char(string='Mã nhân viên', required=True)
    ho_ten = fields.Char(string='Họ và tên', required=True)
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác')
    ], string='Giới tính', default='nam')
    ngay_sinh = fields.Date(string='Ngày sinh')
    tuoi = fields.Integer(string='Tuổi', compute='_compute_tuoi', store=True)
    que_quan = fields.Char(string='Quê quán')
    dia_chi = fields.Char(string='Địa chỉ hiện tại')
    
    # Thông tin liên hệ
    email = fields.Char(string='Email')
    so_dien_thoai = fields.Char(string='Số điện thoại')
    
    # Thông tin công việc
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban')
    chuc_vu_id = fields.Many2one('chuc_vu', string='Chức vụ')
    ngay_vao_lam = fields.Date(string='Ngày vào làm')
    so_nam_cong_tac = fields.Float(string='Số năm công tác', compute='_compute_so_nam_cong_tac')
    trang_thai = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('chinh_thuc', 'Chính thức'),
        ('nghi_phep', 'Nghỉ phép'),
        ('nghi_viec', 'Nghỉ việc')
    ], string='Trạng thái', default='thu_viec')
    
    # Thông tin bổ sung
    cmnd_cccd = fields.Char(string='CMND/CCCD')
    ngay_cap_cmnd = fields.Date(string='Ngày cấp')
    noi_cap_cmnd = fields.Char(string='Nơi cấp')
    so_bhxh = fields.Char(string='Số BHXH')
    so_tai_khoan = fields.Char(string='Số tài khoản ngân hàng')
    ngan_hang = fields.Char(string='Ngân hàng')
    
    active = fields.Boolean(string='Hoạt động', default=True)
    ghi_chu = fields.Text(string='Ghi chú')
    
    # Relationships - Liên kết với các models khác
    cham_cong_ids = fields.One2many('cham_cong', 'nhan_vien_id', string='Lịch sử chấm công')
    bao_cao_cham_cong_ids = fields.One2many('bao_cao_cham_cong', 'nhan_vien_id', string='Báo cáo chấm công')
    bang_luong_ids = fields.One2many('bang_luong', 'nhan_vien_id', string='Lịch sử lương')
    
    # Computed fields - Thống kê
    tong_ngay_cong_thang_nay = fields.Float(string='Tổng công tháng này', compute='_compute_thong_ke_thang')
    luong_thang_nay = fields.Float(string='Lương tháng này', compute='_compute_thong_ke_thang')
    so_lan_di_tre_thang_nay = fields.Integer(string='Số lần đi trễ tháng này', compute='_compute_thong_ke_thang')
    
>>>>>>> cc63fe88 (update)
    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
<<<<<<< HEAD
                today = date.today()
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0

    # ================= CONSTRAINS =================

    @api.constrains('ngay_sinh')
    def _check_ngay_sinh(self):
        for record in self:
            if record.ngay_sinh and record.ngay_sinh > date.today():
                raise ValidationError('Ngày sinh không được là ngày trong tương lai!')
            if record.ngay_sinh and date.today().year - record.ngay_sinh.year > 100:
                raise ValidationError('Tuổi không hợp lệ!')

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.email):
                    raise ValidationError('Định dạng email không hợp lệ!')

    @api.constrains('so_dien_thoai')
    def _check_so_dien_thoai(self):
        for record in self:
            if record.so_dien_thoai:
                phone_regex = r'^[0-9]{10,11}$'
                if not re.match(phone_regex, record.so_dien_thoai):
                    raise ValidationError('Số điện thoại phải có 10-11 chữ số!')

    # ================= ONCHANGE =================

    @api.onchange('chuc_vu_id')
    def _onchange_chuc_vu_id(self):
        if self.chuc_vu_id and self.chuc_vu_id.luong_co_ban and not self.luong:
            self.luong = self.chuc_vu_id.luong_co_ban
=======
                delta = relativedelta(fields.Date.today(), record.ngay_sinh)
                record.tuoi = delta.years
            else:
                record.tuoi = 0
    
    def _compute_so_nam_cong_tac(self):
        for record in self:
            if record.ngay_vao_lam:
                delta = relativedelta(fields.Date.today(), record.ngay_vao_lam)
                record.so_nam_cong_tac = delta.years + (delta.months / 12)
            else:
                record.so_nam_cong_tac = 0
    
    @api.depends('cham_cong_ids', 'bang_luong_ids')
    def _compute_thong_ke_thang(self):
        """Tính toán thống kê cho tháng hiện tại"""
        for record in self:
            today = fields.Date.today()
            thang = today.month
            nam = today.year
            
            # Tổng ngày công tháng này
            cham_cong_thang_nay = record.cham_cong_ids.filtered(
                lambda r: r.ngay_cham_cong.month == thang and r.ngay_cham_cong.year == nam
            )
            record.tong_ngay_cong_thang_nay = len(cham_cong_thang_nay.filtered(lambda r: r.trang_thai in ['du', 'tre', 'som']))
            record.so_lan_di_tre_thang_nay = len(cham_cong_thang_nay.filtered(lambda r: r.trang_thai == 'tre'))
            
            # Lương tháng này
            bang_luong_thang_nay = record.bang_luong_ids.filtered(
                lambda r: r.thang == thang and r.nam == nam
            )
            record.luong_thang_nay = bang_luong_thang_nay[0].thuc_linh if bang_luong_thang_nay else 0
    
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'UNIQUE(ma_dinh_danh)', 'Mã nhân viên phải là duy nhất!'),
    ]
    
    # ==================== ACTION METHODS ====================
    def action_chuyen_chinh_thuc(self):
        """Chuyển nhân viên từ thử việc lên chính thức"""
        for record in self:
            if record.trang_thai == 'thu_viec':
                record.trang_thai = 'chinh_thuc'
        return True
    
    def action_cho_nghi_phep(self):
        """Chuyển nhân viên sang trạng thái nghỉ phép"""
        for record in self:
            if record.trang_thai in ['chinh_thuc', 'thu_viec']:
                record.trang_thai = 'nghi_phep'
        return True
    
    def action_quay_lai_lam_viec(self):
        """Chuyển nhân viên nghỉ phép về lại làm việc"""
        for record in self:
            if record.trang_thai == 'nghi_phep':
                # Quay về trạng thái ban đầu (chính thức hoặc thử việc)
                if record.so_nam_cong_tac >= 0.2:  # >= 2 tháng
                    record.trang_thai = 'chinh_thuc'
                else:
                    record.trang_thai = 'thu_viec'
        return True
    
    def action_nghi_viec(self):
        """Chuyển nhân viên sang trạng thái nghỉ việc và archive"""
        for record in self:
            record.write({
                'trang_thai': 'nghi_viec',
                'active': False
            })
        return True
    
    def action_khoi_phuc_nhan_vien(self):
        """Khôi phục nhân viên đã nghỉ việc"""
        for record in self:
            if record.trang_thai == 'nghi_viec':
                record.write({
                    'trang_thai': 'chinh_thuc',
                    'active': True
                })
        return True
>>>>>>> cc63fe88 (update)
