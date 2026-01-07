# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import re


class NhanVien(models.Model):
    _name = 'nhan_vien'
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

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
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
