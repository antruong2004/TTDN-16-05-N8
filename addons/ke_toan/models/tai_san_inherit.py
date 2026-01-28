# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DanhMucTaiSanKeToanInherit(models.Model):
    """Mở rộng danh mục tài sản với tài khoản kế toán mặc định"""
    _inherit = 'danh_muc_tai_san'

    # Tài khoản kế toán mặc định
    tk_nguyen_gia_id = fields.Many2one(
        'ke_toan.tai_khoan', 
        string='TK Nguyên giá',
        domain=[('nhom_tai_khoan', '=', 'tai_san_co_dinh')],
        help='Tài khoản ghi nhận nguyên giá tài sản (211, 213...)'
    )
    tk_khau_hao_id = fields.Many2one(
        'ke_toan.tai_khoan', 
        string='TK Khấu hao lũy kế',
        domain=[('nhom_tai_khoan', '=', 'tai_san_co_dinh')],
        help='Tài khoản ghi nhận khấu hao lũy kế (2141, 2143...)'
    )
    tk_chi_phi_khau_hao_id = fields.Many2one(
        'ke_toan.tai_khoan', 
        string='TK Chi phí khấu hao',
        domain=[('nhom_tai_khoan', '=', 'chi_phi_khau_hao')],
        help='Tài khoản ghi nhận chi phí khấu hao (6274, 6414...)'
    )


class TaiSanKeToanInherit(models.Model):
    """Mở rộng tài sản với thông tin kế toán"""
    _inherit = 'tai_san'

    # Tài khoản kế toán
    tk_nguyen_gia_id = fields.Many2one(
        'ke_toan.tai_khoan', 
        string='TK Nguyên giá',
        compute='_compute_tai_khoan_ke_toan',
        store=True, readonly=False
    )
    tk_khau_hao_id = fields.Many2one(
        'ke_toan.tai_khoan', 
        string='TK Khấu hao lũy kế',
        compute='_compute_tai_khoan_ke_toan',
        store=True, readonly=False
    )
    tk_chi_phi_khau_hao_id = fields.Many2one(
        'ke_toan.tai_khoan', 
        string='TK Chi phí khấu hao',
        compute='_compute_tai_khoan_ke_toan',
        store=True, readonly=False
    )
    
    # Bút toán liên quan
    but_toan_ids = fields.One2many('ke_toan.but_toan', 'tai_san_id', string='Bút toán kế toán')
    so_but_toan = fields.Integer(string='Số bút toán', compute='_compute_so_but_toan')
    
    # Bút toán mua sắm
    but_toan_mua_sam_id = fields.Many2one('ke_toan.but_toan', string='Bút toán mua sắm',
                                           readonly=True, copy=False)
    da_hach_toan_mua = fields.Boolean(string='Đã hạch toán mua', default=False)

    @api.depends('danh_muc_id', 'danh_muc_id.tk_nguyen_gia_id', 
                 'danh_muc_id.tk_khau_hao_id', 'danh_muc_id.tk_chi_phi_khau_hao_id')
    def _compute_tai_khoan_ke_toan(self):
        for record in self:
            if record.danh_muc_id:
                if not record.tk_nguyen_gia_id:
                    record.tk_nguyen_gia_id = record.danh_muc_id.tk_nguyen_gia_id
                if not record.tk_khau_hao_id:
                    record.tk_khau_hao_id = record.danh_muc_id.tk_khau_hao_id
                if not record.tk_chi_phi_khau_hao_id:
                    record.tk_chi_phi_khau_hao_id = record.danh_muc_id.tk_chi_phi_khau_hao_id

    @api.depends('but_toan_ids')
    def _compute_so_but_toan(self):
        for record in self:
            record.so_but_toan = len(record.but_toan_ids)

    def action_tao_but_toan_mua_sam(self):
        """Tạo bút toán khi mua sắm tài sản"""
        for record in self:
            if record.da_hach_toan_mua:
                continue
            if not record.tk_nguyen_gia_id:
                continue
            
            # Lấy TK tiền từ cấu hình
            config = self.env['res.config.settings']
            tk_tien = config.get_tai_khoan_by_config('ke_toan.tk_ngan_hang_mac_dinh')
            if not tk_tien:
                tk_tien = config.get_tai_khoan_by_config('ke_toan.tk_tien_mat_mac_dinh')
            
            if not tk_tien:
                continue
            
            # Tạo bút toán
            but_toan = self.env['ke_toan.but_toan'].create({
                'loai_chung_tu': 'mua_sam',
                'ngay_chung_tu': record.ngay_mua,
                'dien_giai': f'Mua sắm tài sản: {record.ten_tai_san}',
                'tai_san_id': record.id,
            })
            
            # Nợ TK Nguyên giá TSCĐ
            self.env['ke_toan.but_toan_chi_tiet'].create({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': record.tk_nguyen_gia_id.id,
                'dien_giai': f'Nguyên giá {record.ten_tai_san}',
                'so_tien_no': record.gia_tri_ban_dau,
                'so_tien_co': 0,
            })
            
            # Có TK Tiền/Phải trả
            self.env['ke_toan.but_toan_chi_tiet'].create({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tk_tien.id,
                'dien_giai': f'Chi tiền mua {record.ten_tai_san}',
                'so_tien_no': 0,
                'so_tien_co': record.gia_tri_ban_dau,
            })
            
            record.write({
                'but_toan_mua_sam_id': but_toan.id,
                'da_hach_toan_mua': True,
            })
        
        return True


class KhauHaoKeToanInherit(models.Model):
    """Mở rộng khấu hao với kế toán"""
    _inherit = 'khau_hao'

    # Bút toán kế toán (thay thế liên kết so_cai cũ)
    but_toan_ke_toan_id = fields.Many2one('ke_toan.but_toan', string='Bút toán kế toán',
                                           readonly=True, copy=False)
    da_hach_toan_ke_toan = fields.Boolean(string='Đã hạch toán KT', default=False)

    def action_tao_but_toan_khau_hao(self):
        """Tạo bút toán kế toán cho khấu hao"""
        for record in self:
            if record.da_hach_toan_ke_toan:
                continue
            if record.trang_thai != 'da_ghi_nhan':
                continue
            
            tai_san = record.tai_san_id
            if not tai_san.tk_khau_hao_id or not tai_san.tk_chi_phi_khau_hao_id:
                # Lấy từ cấu hình nếu không có trên tài sản
                config = self.env['res.config.settings']
                tk_khau_hao = config.get_tai_khoan_by_config('ke_toan.tk_khau_hao_mac_dinh')
                tk_chi_phi = config.get_tai_khoan_by_config('ke_toan.tk_chi_phi_khau_hao_mac_dinh')
                
                if not tk_khau_hao or not tk_chi_phi:
                    continue
            else:
                tk_khau_hao = tai_san.tk_khau_hao_id
                tk_chi_phi = tai_san.tk_chi_phi_khau_hao_id
            
            # Tạo bút toán
            but_toan = self.env['ke_toan.but_toan'].create({
                'loai_chung_tu': 'khau_hao',
                'ngay_chung_tu': record.ngay_khau_hao,
                'dien_giai': f'Khấu hao tài sản {tai_san.ten_tai_san} tháng {record.thang_khau_hao}/{record.nam_khau_hao}',
                'tai_san_id': tai_san.id,
                'khau_hao_id': record.id,
            })
            
            # Nợ TK Chi phí khấu hao
            self.env['ke_toan.but_toan_chi_tiet'].create({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tk_chi_phi.id,
                'dien_giai': f'Chi phí khấu hao {tai_san.ten_tai_san}',
                'so_tien_no': record.gia_tri_khau_hao,
                'so_tien_co': 0,
            })
            
            # Có TK Khấu hao lũy kế
            self.env['ke_toan.but_toan_chi_tiet'].create({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tk_khau_hao.id,
                'dien_giai': f'Khấu hao lũy kế {tai_san.ten_tai_san}',
                'so_tien_no': 0,
                'so_tien_co': record.gia_tri_khau_hao,
            })
            
            # Kiểm tra cấu hình tự động duyệt
            tu_dong_duyet = self.env['ir.config_parameter'].sudo().get_param(
                'ke_toan.tu_dong_duyet_but_toan_khau_hao', 'False'
            )
            if tu_dong_duyet == 'True':
                but_toan.action_gui_duyet()
                but_toan.action_duyet()
            
            record.write({
                'but_toan_ke_toan_id': but_toan.id,
                'da_hach_toan_ke_toan': True,
            })
        
        return True
    
    def action_huy_but_toan_khau_hao(self):
        """Hủy bút toán kế toán khi hủy khấu hao"""
        for record in self:
            if record.but_toan_ke_toan_id:
                if record.but_toan_ke_toan_id.trang_thai != 'da_ghi_so':
                    record.but_toan_ke_toan_id.unlink()
                else:
                    record.but_toan_ke_toan_id.action_huy()
                record.but_toan_ke_toan_id = False
                record.da_hach_toan_ke_toan = False
        return True


class ThanhLyTaiSanKeToanInherit(models.Model):
    """Mở rộng thanh lý tài sản với kế toán"""
    _inherit = 'thanh_ly_tai_san'

    # Bút toán kế toán
    but_toan_thanh_ly_id = fields.Many2one('ke_toan.but_toan', string='Bút toán thanh lý',
                                            readonly=True, copy=False)
    da_hach_toan_thanh_ly = fields.Boolean(string='Đã hạch toán', default=False)

    def action_tao_but_toan_thanh_ly(self):
        """Tạo bút toán thanh lý tài sản"""
        for record in self:
            if record.da_hach_toan_thanh_ly:
                continue
            if record.trang_thai != 'hoan_thanh':
                continue
            
            tai_san = record.tai_san_id
            if not tai_san.tk_nguyen_gia_id or not tai_san.tk_khau_hao_id:
                continue
            
            # Lấy tài khoản từ cấu hình
            config = self.env['res.config.settings']
            tk_thu_nhap = config.get_tai_khoan_by_config('ke_toan.tk_thu_nhap_khac')
            tk_tien = config.get_tai_khoan_by_config('ke_toan.tk_tien_mat_mac_dinh')
            if not tk_tien:
                tk_tien = config.get_tai_khoan_by_config('ke_toan.tk_ngan_hang_mac_dinh')
            
            # Tạo bút toán
            but_toan = self.env['ke_toan.but_toan'].create({
                'loai_chung_tu': 'thanh_ly',
                'ngay_chung_tu': record.ngay_thanh_ly,
                'dien_giai': f'Thanh lý tài sản: {tai_san.ten_tai_san}',
                'tai_san_id': tai_san.id,
            })
            
            chi_tiet = []
            
            # Nợ TK Khấu hao lũy kế (xóa sổ KH)
            chi_tiet.append({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tai_san.tk_khau_hao_id.id,
                'dien_giai': f'Xóa sổ khấu hao lũy kế',
                'so_tien_no': tai_san.tong_khau_hao,
                'so_tien_co': 0,
            })
            
            # Có TK Nguyên giá (xóa sổ NG)
            chi_tiet.append({
                'but_toan_id': but_toan.id,
                'tai_khoan_id': tai_san.tk_nguyen_gia_id.id,
                'dien_giai': f'Xóa sổ nguyên giá',
                'so_tien_no': 0,
                'so_tien_co': tai_san.gia_tri_ban_dau,
            })
            
            # Nếu có thu hồi tiền
            if record.gia_tri_thu_hoi > 0 and tk_tien:
                chi_tiet.append({
                    'but_toan_id': but_toan.id,
                    'tai_khoan_id': tk_tien.id,
                    'dien_giai': 'Thu tiền thanh lý',
                    'so_tien_no': record.gia_tri_thu_hoi,
                    'so_tien_co': 0,
                })
                if tk_thu_nhap:
                    chi_tiet.append({
                        'but_toan_id': but_toan.id,
                        'tai_khoan_id': tk_thu_nhap.id,
                        'dien_giai': 'Thu nhập từ thanh lý',
                        'so_tien_no': 0,
                        'so_tien_co': record.gia_tri_thu_hoi,
                    })
            
            # Ghi nhận lỗ nếu giá trị còn lại > thu hồi
            gia_tri_con_lai = tai_san.gia_tri_ban_dau - tai_san.tong_khau_hao
            chenh_lech = gia_tri_con_lai - record.gia_tri_thu_hoi
            if chenh_lech > 0:
                tk_chi_phi_khac = config.get_tai_khoan_by_config('ke_toan.tk_chi_phi_khac')
                if tk_chi_phi_khac:
                    chi_tiet.append({
                        'but_toan_id': but_toan.id,
                        'tai_khoan_id': tk_chi_phi_khac.id,
                        'dien_giai': 'Lỗ thanh lý TSCĐ',
                        'so_tien_no': chenh_lech,
                        'so_tien_co': 0,
                    })
            
            for ct in chi_tiet:
                self.env['ke_toan.but_toan_chi_tiet'].create(ct)
            
            record.write({
                'but_toan_thanh_ly_id': but_toan.id,
                'da_hach_toan_thanh_ly': True,
            })
        
        return True
