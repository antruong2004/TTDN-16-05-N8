# -*- coding: utf-8 -*-
<<<<<<< HEAD

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
=======
from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
>>>>>>> cc63fe88 (update)


class ChamCong(models.Model):
    _name = 'cham_cong'
<<<<<<< HEAD
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

=======
    _description = 'Chấm công nhân viên'
    _order = 'ngay_cham_cong desc, gio_vao desc'
    _rec_name = 'nhan_vien_id'

    # Thông tin cơ bản
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', related='nhan_vien_id.phong_ban_id', store=True)
    ngay_cham_cong = fields.Date(string='Ngày chấm công', required=True, default=fields.Date.today)
    
    # Thời gian vào ra
    gio_vao = fields.Datetime(string='Giờ vào')
    gio_ra = fields.Datetime(string='Giờ ra')
    
    # Tính toán tự động
    so_gio_lam = fields.Float(string='Số giờ làm việc', compute='_compute_so_gio_lam', store=True)
    so_gio_tang_ca = fields.Float(string='Số giờ tăng ca', default=0)
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('du', 'Đủ công'),
        ('tre', 'Đi trễ'),
        ('som', 'Về sớm'),
        ('nghi_co_phep', 'Nghỉ có phép'),
        ('nghi_khong_phep', 'Nghỉ không phép'),
        ('nghi_le', 'Nghỉ lễ')
    ], string='Trạng thái', default='du')
    
    # Loại công
    loai_cong = fields.Selection([
        ('binh_thuong', 'Bình thường'),
        ('nghi_phep', 'Nghỉ phép'),
        ('nghi_om', 'Nghỉ ốm'),
        ('cong_tac', 'Công tác'),
        ('nghi_le', 'Nghỉ lễ')
    ], string='Loại công', default='binh_thuong')
    
    ghi_chu = fields.Text(string='Ghi chú')
    
    # Giờ quy định
    gio_vao_quy_dinh = fields.Float(string='Giờ vào quy định', default=8.0)
    gio_ra_quy_dinh = fields.Float(string='Giờ ra quy định', default=17.0)
    
>>>>>>> cc63fe88 (update)
    @api.depends('gio_vao', 'gio_ra')
    def _compute_so_gio_lam(self):
        for record in self:
            if record.gio_vao and record.gio_ra:
                delta = record.gio_ra - record.gio_vao
<<<<<<< HEAD
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
=======
                record.so_gio_lam = delta.total_seconds() / 3600  # Chuyển sang giờ
                
                # Kiểm tra đi trễ hoặc về sớm
                gio_vao_time = record.gio_vao.hour + record.gio_vao.minute / 60
                gio_ra_time = record.gio_ra.hour + record.gio_ra.minute / 60
                
                if gio_vao_time > record.gio_vao_quy_dinh:
                    record.trang_thai = 'tre'
                elif gio_ra_time < record.gio_ra_quy_dinh:
                    record.trang_thai = 'som'
                else:
                    record.trang_thai = 'du'
            else:
                record.so_gio_lam = 0
    
    @api.constrains('gio_vao', 'gio_ra')
    def _check_gio_vao_ra(self):
        for record in self:
            if record.gio_vao and record.gio_ra:
                if record.gio_ra <= record.gio_vao:
                    raise exceptions.ValidationError('Giờ ra phải sau giờ vào!')
    
    @api.model
    def check_in(self, nhan_vien_id):
        """Hàm check-in cho nhân viên"""
        existing = self.search([
            ('nhan_vien_id', '=', nhan_vien_id),
            ('ngay_cham_cong', '=', fields.Date.today())
        ], limit=1)
        
        if existing and existing.gio_vao:
            raise exceptions.UserError('Nhân viên đã check-in hôm nay!')
        
        if existing:
            existing.write({'gio_vao': fields.Datetime.now()})
            return existing
        else:
            return self.create({
                'nhan_vien_id': nhan_vien_id,
                'ngay_cham_cong': fields.Date.today(),
                'gio_vao': fields.Datetime.now()
            })
    
    @api.model
    def check_out(self, nhan_vien_id):
        """Hàm check-out cho nhân viên"""
        existing = self.search([
            ('nhan_vien_id', '=', nhan_vien_id),
            ('ngay_cham_cong', '=', fields.Date.today())
        ], limit=1)
        
        if not existing or not existing.gio_vao:
            raise exceptions.UserError('Nhân viên chưa check-in hôm nay!')
        
        if existing.gio_ra:
            raise exceptions.UserError('Nhân viên đã check-out hôm nay!')
        
        existing.write({'gio_ra': fields.Datetime.now()})
        return existing


class BaoCaoChamCong(models.Model):
    _name = 'bao_cao_cham_cong'
    _description = 'Báo cáo chấm công tháng'
    _order = 'thang desc, nam desc'

    # Thông tin kỳ báo cáo
    thang = fields.Integer(string='Tháng', required=True)
    nam = fields.Integer(string='Năm', required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', related='nhan_vien_id.phong_ban_id', store=True)
    
    # Thống kê
    tong_ngay_cong = fields.Float(string='Tổng ngày công', compute='_compute_thong_ke', store=True)
    ngay_di_tre = fields.Integer(string='Số ngày đi trễ', compute='_compute_thong_ke', store=True)
    ngay_ve_som = fields.Integer(string='Số ngày về sớm', compute='_compute_thong_ke', store=True)
    ngay_nghi_co_phep = fields.Integer(string='Nghỉ có phép', compute='_compute_thong_ke', store=True)
    ngay_nghi_khong_phep = fields.Integer(string='Nghỉ không phép', compute='_compute_thong_ke', store=True)
    tong_gio_lam = fields.Float(string='Tổng giờ làm việc', compute='_compute_thong_ke', store=True)
    tong_gio_tang_ca = fields.Float(string='Tổng giờ tăng ca', compute='_compute_thong_ke', store=True)
    
    ghi_chu = fields.Text(string='Ghi chú')
    
    @api.depends('thang', 'nam', 'nhan_vien_id')
    def _compute_thong_ke(self):
        for record in self:
            if not record.thang or not record.nam or not record.nhan_vien_id:
                record.tong_ngay_cong = 0
                record.ngay_di_tre = 0
                record.ngay_ve_som = 0
                record.ngay_nghi_co_phep = 0
                record.ngay_nghi_khong_phep = 0
                record.tong_gio_lam = 0
                record.tong_gio_tang_ca = 0
                continue
            
            # Tìm tất cả bản ghi chấm công trong tháng
            date_from = datetime(record.nam, record.thang, 1).date()
            if record.thang == 12:
                date_to = datetime(record.nam + 1, 1, 1).date()
            else:
                date_to = datetime(record.nam, record.thang + 1, 1).date()
            
            cham_cong_records = self.env['cham_cong'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', date_from),
                ('ngay_cham_cong', '<', date_to)
            ])
            
            # Tính toán
            record.tong_ngay_cong = sum(1 for r in cham_cong_records if r.trang_thai in ['du', 'tre', 'som'])
            record.ngay_di_tre = sum(1 for r in cham_cong_records if r.trang_thai == 'tre')
            record.ngay_ve_som = sum(1 for r in cham_cong_records if r.trang_thai == 'som')
            record.ngay_nghi_co_phep = sum(1 for r in cham_cong_records if r.trang_thai == 'nghi_co_phep')
            record.ngay_nghi_khong_phep = sum(1 for r in cham_cong_records if r.trang_thai == 'nghi_khong_phep')
            record.tong_gio_lam = sum(cham_cong_records.mapped('so_gio_lam'))
            record.tong_gio_tang_ca = sum(cham_cong_records.mapped('so_gio_tang_ca'))
    
    _sql_constraints = [
        ('nhan_vien_thang_nam_unique', 'UNIQUE(nhan_vien_id, thang, nam)', 
         'Đã tồn tại báo cáo chấm công cho nhân viên này trong tháng này!')
    ]
>>>>>>> cc63fe88 (update)
