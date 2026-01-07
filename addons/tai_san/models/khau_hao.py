# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KhauHao(models.Model):
    _name = 'khau_hao'
    _description = 'Khấu hao tài sản'
    _rec_name = 'ten_khau_hao'
    _order = 'nam desc, thang desc, id desc'
    
    _sql_constraints = [
        ('tai_san_thang_nam_unique', 'unique(tai_san_id, thang, nam)', 
         'Tài sản chỉ có một bản ghi khấu hao cho mỗi tháng!'),
    ]

    ten_khau_hao = fields.Char(
        string="Tên",
        compute='_compute_ten_khau_hao',
        store=True
    )
    
    tai_san_id = fields.Many2one(
        comodel_name='tai_san',
        string="Tài sản",
        required=True,
        ondelete='cascade'
    )
    
    ma_tai_san = fields.Char(
        related='tai_san_id.ma_tai_san',
        string="Mã tài sản",
        store=True
    )
    
    ten_tai_san = fields.Char(
        related='tai_san_id.ten_tai_san',
        string="Tên tài sản",
        store=True
    )
    
    thang = fields.Integer(
        string="Tháng",
        required=True
    )
    
    nam = fields.Integer(
        string="Năm",
        required=True
    )
    
    gia_tri_khau_hao = fields.Float(
        string="Giá trị khấu hao",
        required=True,
        digits=(16, 2)
    )
    
    gia_tri_con_lai = fields.Float(
        string="Giá trị còn lại sau khấu hao",
        compute='_compute_gia_tri_con_lai',
        store=True,
        digits=(16, 2)
    )
    
    ngay_ghi_nhan = fields.Date(
        string="Ngày ghi nhận",
        default=fields.Date.context_today,
        required=True
    )
    
    ghi_chu = fields.Text(string="Ghi chú")

    @api.depends('tai_san_id.ten_tai_san', 'thang', 'nam')
    def _compute_ten_khau_hao(self):
        for record in self:
            if record.tai_san_id and record.thang and record.nam:
                record.ten_khau_hao = f"Khấu hao {record.tai_san_id.ten_tai_san} - {record.thang}/{record.nam}"
            else:
                record.ten_khau_hao = "Khấu hao"

    @api.depends('tai_san_id.nguyen_gia', 'tai_san_id.gia_tri_khau_hao_luy_ke')
    def _compute_gia_tri_con_lai(self):
        for record in self:
            if record.tai_san_id:
                # Tính giá trị còn lại trước khi khấu hao bản ghi này
                gia_tri_khau_hao_truoc = sum(
                    record.tai_san_id.khau_hao_ids.filtered(
                        lambda x: x.id != record.id
                    ).mapped('gia_tri_khau_hao')
                )
                record.gia_tri_con_lai = record.tai_san_id.nguyen_gia - gia_tri_khau_hao_truoc - record.gia_tri_khau_hao
            else:
                record.gia_tri_con_lai = 0.0

    @api.constrains('thang')
    def _check_thang(self):
        for record in self:
            if record.thang < 1 or record.thang > 12:
                raise ValidationError(_('Tháng phải từ 1 đến 12!'))

    @api.constrains('nam')
    def _check_nam(self):
        for record in self:
            if record.nam < 1900 or record.nam > 2100:
                raise ValidationError(_('Năm không hợp lệ!'))

    @api.constrains('gia_tri_khau_hao')
    def _check_gia_tri_khau_hao(self):
        for record in self:
            if record.gia_tri_khau_hao <= 0:
                raise ValidationError(_('Giá trị khấu hao phải lớn hơn 0!'))
            
            # Kiểm tra không vượt quá giá trị còn lại
            gia_tri_khau_hao_truoc = sum(
                record.tai_san_id.khau_hao_ids.filtered(
                    lambda x: x.id != record.id
                ).mapped('gia_tri_khau_hao')
            )
            gia_tri_con_lai_truoc_khi_khau_hao = record.tai_san_id.nguyen_gia - gia_tri_khau_hao_truoc
            
            if record.gia_tri_khau_hao > gia_tri_con_lai_truoc_khi_khau_hao:
                raise ValidationError(_(
                    'Giá trị khấu hao (%s) không thể lớn hơn giá trị còn lại của tài sản (%s)!'
                ) % (record.gia_tri_khau_hao, gia_tri_con_lai_truoc_khi_khau_hao))

    @api.model
    def create(self, vals):
        """Tự động tạo bút toán kế toán khi tạo khấu hao"""
        record = super(KhauHao, self).create(vals)
        
        # Tạo bút toán kế toán tự động (nếu module kế toán đã cài)
        if self.env['ir.module.module'].search([('name', '=', 'ke_toan'), ('state', '=', 'installed')]):
            record._tao_but_toan_ke_toan()
        
        return record

    def _tao_but_toan_ke_toan(self):
        """Tạo bút toán kế toán cho khấu hao"""
        self.ensure_one()
        
        # Kiểm tra module ke_toan có cài không
        if 'so_cai' not in self.env:
            return
        
        SoCai = self.env['so_cai']
        
        # Tìm tài khoản kế toán
        tk_chi_phi_khau_hao = self.env['tai_khoan_ke_toan'].search([
            ('ma_tai_khoan', '=', '627')  # Chi phí khấu hao TSCĐ
        ], limit=1)
        
        tk_khau_hao_luy_ke = self.env['tai_khoan_ke_toan'].search([
            ('ma_tai_khoan', '=', '214')  # Hao mòn TSCĐ
        ], limit=1)
        
        if not tk_chi_phi_khau_hao or not tk_khau_hao_luy_ke:
            return  # Không tạo nếu chưa có tài khoản
        
        # Tạo bút toán và liên kết với khấu hao này
        so_cai = SoCai.create({
            'ngay_ghi_so': self.ngay_ghi_nhan,
            'dien_giai': f'Khấu hao {self.tai_san_id.ten_tai_san} tháng {self.thang}/{self.nam}',
            'tai_khoan_no_id': tk_chi_phi_khau_hao.id,
            'tai_khoan_co_id': tk_khau_hao_luy_ke.id,
            'so_tien': self.gia_tri_khau_hao,
            'loai_chung_tu': 'khau_hao',
            'ma_chung_tu': f'KH-{self.tai_san_id.ma_tai_san}-{self.thang:02d}{self.nam}',
        })
        
        # Liên kết ngược nếu field so_cai_id tồn tại (khi module ke_toan đã cài)
        if hasattr(self, 'so_cai_id'):
            self.so_cai_id = so_cai.id
