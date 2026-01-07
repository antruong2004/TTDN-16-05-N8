# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Chấm công'
    _order = 'ngay_lam desc'

    _sql_constraints = [
        ('unique_nhan_vien_ngay',
         'unique(nhan_vien_id, ngay_lam)',
         'Nhân viên đã có bản ghi chấm công cho ngày này!'),
    ]

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    ngay_lam = fields.Date(
        string="Ngày làm",
        required=True,
        default=fields.Date.context_today,
        index=True
    )

    gio_vao = fields.Datetime(
        string="Giờ vào"
    )

    gio_ra = fields.Datetime(
        string="Giờ ra"
    )

    so_gio_lam = fields.Float(
        string="Số giờ làm",
        compute='_compute_so_gio_lam',
        store=True,
        digits=(16, 2)
    )

    loai_cham_cong = fields.Selection(
        selection=[
            ('di_lam', 'Đi làm'),
            ('nghi_phep', 'Nghỉ phép'),
            ('nghi_khong_phep', 'Nghỉ không phép'),
            ('nghi_om', 'Nghỉ ốm'),
            ('lam_them', 'Làm thêm'),
            ('dot_xuat', 'Đột xuất'),
        ],
        string="Loại chấm công",
        required=True,
        default='di_lam'
    )

    trang_thai = fields.Selection(
        selection=[
            ('chua_duyet', 'Chưa duyệt'),
            ('da_duyet', 'Đã duyệt'),
        ],
        string="Trạng thái",
        default='chua_duyet'
    )

    ly_do = fields.Text(string="Lý do")
    ghi_chu = fields.Text(string="Ghi chú")

    # ================= COMPUTE =================

    @api.depends('gio_vao', 'gio_ra')
    def _compute_so_gio_lam(self):
        for record in self:
            if record.gio_vao and record.gio_ra:
                delta = record.gio_ra - record.gio_vao
                if delta.total_seconds() < 0:
                    raise ValidationError('Giờ ra phải sau giờ vào!')
                record.so_gio_lam = delta.total_seconds() / 3600
            else:
                record.so_gio_lam = 0

    # ================= CONSTRAINS =================

    @api.constrains('ngay_lam')
    def _check_ngay_lam(self):
        for record in self:
            if record.ngay_lam and record.ngay_lam > date.today():
                raise ValidationError('Không thể chấm công cho ngày trong tương lai!')

    # ================= ONCHANGE =================

    @api.onchange('loai_cham_cong')
    def _onchange_loai_cham_cong(self):
        if self.loai_cham_cong in ['nghi_phep', 'nghi_khong_phep', 'nghi_om']:
            self.gio_vao = False
            self.gio_ra = False
            self.so_gio_lam = 0
