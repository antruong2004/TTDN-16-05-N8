# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ===== CẤU HÌNH TÀI KHOẢN KẾ TOÁN MẶC ĐỊNH =====
    
    # Tài khoản cho tài sản cố định
    tk_nguyen_gia_mac_dinh_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Nguyên giá TSCĐ mặc định',
        domain=[('nhom_tai_khoan', '=', 'tai_san_co_dinh')],
        config_parameter='ke_toan.tk_nguyen_gia_mac_dinh',
        help='Tài khoản 211 - Nguyên giá tài sản cố định hữu hình'
    )
    
    tk_khau_hao_mac_dinh_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Khấu hao lũy kế mặc định',
        domain=[('nhom_tai_khoan', '=', 'tai_san_co_dinh')],
        config_parameter='ke_toan.tk_khau_hao_mac_dinh',
        help='Tài khoản 214 - Hao mòn tài sản cố định'
    )
    
    tk_chi_phi_khau_hao_mac_dinh_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Chi phí khấu hao mặc định',
        domain=[('nhom_tai_khoan', '=', 'chi_phi_khau_hao')],
        config_parameter='ke_toan.tk_chi_phi_khau_hao_mac_dinh',
        help='Tài khoản 6274/6414 - Chi phí khấu hao TSCĐ'
    )
    
    # Tài khoản cho thanh lý
    tk_thu_nhap_khac_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Thu nhập khác',
        domain=[('nhom_tai_khoan', '=', 'doanh_thu')],
        config_parameter='ke_toan.tk_thu_nhap_khac',
        help='Tài khoản 711 - Thu nhập khác'
    )
    
    tk_chi_phi_khac_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Chi phí khác',
        domain=[('nhom_tai_khoan', '=', 'chi_phi_khac')],
        config_parameter='ke_toan.tk_chi_phi_khac',
        help='Tài khoản 811 - Chi phí khác'
    )
    
    # Tài khoản tiền mặt/ngân hàng
    tk_tien_mat_mac_dinh_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Tiền mặt mặc định',
        domain=[('nhom_tai_khoan', '=', 'tien_te')],
        config_parameter='ke_toan.tk_tien_mat_mac_dinh',
        help='Tài khoản 111 - Tiền mặt'
    )
    
    tk_ngan_hang_mac_dinh_id = fields.Many2one(
        'ke_toan.tai_khoan',
        string='TK Ngân hàng mặc định',
        domain=[('nhom_tai_khoan', '=', 'tien_te')],
        config_parameter='ke_toan.tk_ngan_hang_mac_dinh',
        help='Tài khoản 112 - Tiền gửi ngân hàng'
    )
    
    # ===== CẤU HÌNH CHUNG =====
    
    tu_dong_tao_but_toan_khau_hao = fields.Boolean(
        string='Tự động tạo bút toán khấu hao',
        config_parameter='ke_toan.tu_dong_tao_but_toan_khau_hao',
        default=True,
        help='Tự động tạo bút toán kế toán khi ghi nhận khấu hao'
    )
    
    tu_dong_duyet_but_toan_khau_hao = fields.Boolean(
        string='Tự động duyệt bút toán khấu hao',
        config_parameter='ke_toan.tu_dong_duyet_but_toan_khau_hao',
        default=False,
        help='Tự động duyệt và ghi sổ bút toán khấu hao (không cần phê duyệt)'
    )
    
    cho_phep_sua_tai_khoan_tai_san = fields.Boolean(
        string='Cho phép sửa tài khoản trên tài sản',
        config_parameter='ke_toan.cho_phep_sua_tai_khoan_tai_san',
        default=True,
        help='Cho phép thay đổi tài khoản kế toán trên từng tài sản cụ thể'
    )

    @api.model
    def get_tai_khoan_by_config(self, config_key):
        """
        Lấy tài khoản kế toán từ cấu hình
        
        Args:
            config_key: Khóa cấu hình (vd: 'ke_toan.tk_chi_phi_khau_hao_mac_dinh')
            
        Returns:
            recordset của ke_toan.tai_khoan hoặc False
        """
        tk_id = int(self.env['ir.config_parameter'].sudo().get_param(config_key, 0))
        if tk_id:
            return self.env['ke_toan.tai_khoan'].browse(tk_id).exists()
        return self.env['ke_toan.tai_khoan']
