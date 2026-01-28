# -*- coding: utf-8 -*-

from odoo import models, fields, api


<<<<<<< HEAD
class NhanVienInherit(models.Model):
    _inherit = 'nhan_vien'

    so_cai_lap_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='nguoi_lap_id',
        string='Chứng từ đã lập'
    )
    
    so_cai_duyet_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='nguoi_duyet_id',
        string='Chứng từ đã duyệt'
    )
    
    so_luong_chung_tu_lap = fields.Integer(
        string="Số chứng từ đã lập",
        compute='_compute_so_luong_chung_tu',
        store=True
    )
    
    so_luong_chung_tu_duyet = fields.Integer(
        string="Số chứng từ đã duyệt",
        compute='_compute_so_luong_chung_tu',
        store=True
    )

    @api.depends('so_cai_lap_ids', 'so_cai_duyet_ids')
    def _compute_so_luong_chung_tu(self):
        for record in self:
            record.so_luong_chung_tu_lap = len(record.so_cai_lap_ids)
            record.so_luong_chung_tu_duyet = len(record.so_cai_duyet_ids)


class PhongBanInherit(models.Model):
    _inherit = 'phong_ban'

    so_cai_ids = fields.One2many(
        comodel_name='so_cai',
        inverse_name='phong_ban_id',
        string='Chứng từ của phòng ban'
    )
    
    so_luong_chung_tu = fields.Integer(
        string="Số chứng từ",
        compute='_compute_so_luong_chung_tu',
        store=True
    )
    
    tong_gia_tri_chung_tu = fields.Float(
        string="Tổng giá trị chứng từ",
        compute='_compute_tong_gia_tri_chung_tu',
        digits=(16, 2)
    )

    @api.depends('so_cai_ids')
    def _compute_so_luong_chung_tu(self):
        for record in self:
            record.so_luong_chung_tu = len(record.so_cai_ids)
    
    @api.depends('so_cai_ids.so_tien')
    def _compute_tong_gia_tri_chung_tu(self):
        for record in self:
            record.tong_gia_tri_chung_tu = sum(record.so_cai_ids.mapped('so_tien'))
=======
class NhanVienKeToanInherit(models.Model):
    """Mở rộng nhân viên với thông tin kế toán"""
    _inherit = 'nhan_vien'

    # Tài khoản kế toán liên quan
    tk_luong_id = fields.Many2one('ke_toan.tai_khoan', string='TK tiền lương',
                                   domain=[('nhom_tai_khoan', '=', 'chi_phi_nhan_su')],
                                   help='Tài khoản ghi nhận chi phí lương')
    tk_bhxh_id = fields.Many2one('ke_toan.tai_khoan', string='TK BHXH',
                                  help='Tài khoản ghi nhận BHXH')
    
    # Thống kê kế toán
    but_toan_ids = fields.One2many('ke_toan.but_toan', 'nhan_vien_id', string='Bút toán liên quan')
    tong_chi_phi_luong = fields.Float(string='Tổng chi phí lương', 
                                       compute='_compute_thong_ke_ke_toan')
    tong_but_toan = fields.Integer(string='Số bút toán', 
                                    compute='_compute_thong_ke_ke_toan')

    @api.depends('but_toan_ids', 'but_toan_ids.trang_thai', 'but_toan_ids.tong_no')
    def _compute_thong_ke_ke_toan(self):
        for record in self:
            but_toan_da_ghi = record.but_toan_ids.filtered(lambda b: b.trang_thai == 'da_ghi_so')
            record.tong_but_toan = len(but_toan_da_ghi)
            record.tong_chi_phi_luong = sum(but_toan_da_ghi.filtered(
                lambda b: b.loai_chung_tu == 'luong'
            ).mapped('tong_no'))


class PhongBanKeToanInherit(models.Model):
    """Mở rộng phòng ban với thông tin kế toán"""
    _inherit = 'phong_ban'

    # Tài khoản chi phí mặc định
    tk_chi_phi_id = fields.Many2one('ke_toan.tai_khoan', string='TK chi phí',
                                     domain=[('loai_tai_khoan', '=', 'chi_phi')],
                                     help='Tài khoản chi phí mặc định cho phòng ban')
    
    # Thống kê
    tong_chi_phi_ky_nay = fields.Float(string='Tổng chi phí kỳ này',
                                        compute='_compute_chi_phi_phong_ban')

    def _compute_chi_phi_phong_ban(self):
        for record in self:
            # Tìm kỳ kế toán hiện tại
            ky_hien_tai = self.env['ke_toan.ky'].search([
                ('trang_thai', '=', 'mo'),
            ], order='ngay_bat_dau desc', limit=1)
            
            if ky_hien_tai and record.tk_chi_phi_id:
                # Tổng phát sinh Nợ của TK chi phí
                but_toan = self.env['ke_toan.but_toan_chi_tiet'].search([
                    ('tai_khoan_id', '=', record.tk_chi_phi_id.id),
                    ('but_toan_id.ky_ke_toan_id', '=', ky_hien_tai.id),
                    ('but_toan_id.trang_thai', '=', 'da_ghi_so'),
                ])
                record.tong_chi_phi_ky_nay = sum(but_toan.mapped('so_tien_no'))
            else:
                record.tong_chi_phi_ky_nay = 0.0


class BangLuongKeToanInherit(models.Model):
    """Mở rộng bảng lương với kế toán"""
    _inherit = 'bang_luong'

    # Bút toán kế toán
    but_toan_id = fields.Many2one('ke_toan.but_toan', string='Bút toán kế toán',
                                   readonly=True, copy=False)
    da_hach_toan = fields.Boolean(string='Đã hạch toán', default=False)

    def action_tao_but_toan(self):
        """Tạo bút toán kế toán cho bảng lương"""
        for record in self:
            if record.da_hach_toan:
                continue
            if record.trang_thai != 'da_duyet':
                continue
            
            # Tìm tài khoản
            tk_luong = self.env['ke_toan.tai_khoan'].search([
                ('ma_tai_khoan', '=', '334')
            ], limit=1)
            tk_chi_phi = self.env['ke_toan.tai_khoan'].search([
                ('ma_tai_khoan', '=', '642')
            ], limit=1)
            tk_bhxh = self.env['ke_toan.tai_khoan'].search([
                ('ma_tai_khoan', '=', '3383')
            ], limit=1)
            
            if not tk_luong or not tk_chi_phi:
                continue
            
            # Tạo bút toán
            but_toan = self.env['ke_toan.but_toan'].create({
                'loai_chung_tu': 'luong',
                'ngay_chung_tu': record.ngay_tinh_luong or fields.Date.today(),
                'dien_giai': f'Chi phí lương tháng {record.thang}/{record.nam} - {record.nhan_vien_id.ho_ten}',
                'nhan_vien_id': record.nhan_vien_id.id,
                'bang_luong_id': record.id,
            })
            
            # Chi tiết: Nợ TK chi phí
            self.env['ke_toan.but_toan_chi_tiet'].create({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tk_chi_phi.id,
                'dien_giai': 'Chi phí lương',
                'so_tien_no': record.tong_thu_nhap,
                'so_tien_co': 0,
            })
            
            # Chi tiết: Có TK lương phải trả
            self.env['ke_toan.but_toan_chi_tiet'].create({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tk_luong.id,
                'dien_giai': 'Lương phải trả',
                'so_tien_no': 0,
                'so_tien_co': record.luong_thuc_linh,
            })
            
            # Chi tiết: Có TK BHXH nếu có
            if tk_bhxh and record.tong_khau_tru > 0:
                self.env['ke_toan.but_toan_chi_tiet'].create({
                    'but_toan_id': but_toan.id,
                    'tai_khoan_id': tk_bhxh.id,
                    'dien_giai': 'Các khoản trích theo lương',
                    'so_tien_no': 0,
                    'so_tien_co': record.tong_khau_tru,
                })
            
            record.write({
                'but_toan_id': but_toan.id,
                'da_hach_toan': True,
            })
        
        return True
>>>>>>> cc63fe88 (update)
