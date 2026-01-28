# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NhanVienTaiSanInherit(models.Model):
    """Thêm thông tin tài sản cho nhân viên từ module Quản lý Tài sản"""
    _inherit = 'nhan_vien'

    # Relationships - Liên kết với tài sản
    tai_san_quan_ly_ids = fields.One2many(
        'tai_san', 
        'nguoi_quan_ly_id', 
        string='Tài sản đang quản lý',
        help='Danh sách tài sản mà nhân viên này đang quản lý'
    )
    
    phan_bo_tai_san_ids = fields.One2many(
        'phan_bo_tai_san',
        'nhan_vien_id',
        string='Lịch sử phân bổ tài sản'
    )
    
    muon_tai_san_ids = fields.One2many(
        'muon_tra_tai_san',
        'nhan_vien_id',
        string='Lịch sử mượn tài sản'
    )
    
    # Computed fields - Thống kê tài sản
    so_tai_san_dang_quan_ly = fields.Integer(
        string='Số TS đang quản lý',
        compute='_compute_thong_ke_tai_san',
        store=True
    )
    
    tong_gia_tri_tai_san_quan_ly = fields.Float(
        string='Tổng giá trị TS',
        compute='_compute_thong_ke_tai_san',
        store=True
    )
    
    so_tai_san_dang_muon = fields.Integer(
        string='Số TS đang mượn',
        compute='_compute_so_tai_san_dang_muon'
    )
    
    @api.depends('tai_san_quan_ly_ids', 'tai_san_quan_ly_ids.gia_tri_con_lai', 'tai_san_quan_ly_ids.trang_thai')
    def _compute_thong_ke_tai_san(self):
        for record in self:
            # Đếm tài sản đang quản lý (chỉ đếm tài sản đang sử dụng)
            tai_san_dang_quan_ly = record.tai_san_quan_ly_ids.filtered(
                lambda ts: ts.trang_thai == 'dang_su_dung'
            )
            record.so_tai_san_dang_quan_ly = len(tai_san_dang_quan_ly)
            record.tong_gia_tri_tai_san_quan_ly = sum(tai_san_dang_quan_ly.mapped('gia_tri_con_lai'))
    
    @api.depends('muon_tai_san_ids', 'muon_tai_san_ids.trang_thai')
    def _compute_so_tai_san_dang_muon(self):
        for record in self:
            # Đếm tài sản đang mượn (chưa trả)
            muon_chua_tra = record.muon_tai_san_ids.filtered(
                lambda m: m.trang_thai == 'dang_muon'
            )
            record.so_tai_san_dang_muon = len(muon_chua_tra)


class PhongBanTaiSanInherit(models.Model):
    """Thêm thông tin tài sản cho phòng ban từ module Quản lý Tài sản"""
    _inherit = 'phong_ban'

    # Relationships - Liên kết với tài sản
    tai_san_phong_ban_ids = fields.One2many(
        'tai_san',
        'phong_ban_id',
        string='Tài sản của phòng ban',
        help='Danh sách tài sản thuộc phòng ban'
    )
    
    phan_bo_tai_san_phong_ban_ids = fields.One2many(
        'phan_bo_tai_san',
        'phong_ban_id',
        string='Lịch sử phân bổ tài sản'
    )
    
    # Computed fields - Thống kê tài sản
    so_tai_san_phong_ban = fields.Integer(
        string='Số tài sản',
        compute='_compute_thong_ke_tai_san_pb',
        store=True
    )
    
    so_tai_san_dang_su_dung_pb = fields.Integer(
        string='TS đang sử dụng',
        compute='_compute_thong_ke_tai_san_pb',
        store=True
    )
    
    tong_gia_tri_tai_san_pb = fields.Float(
        string='Tổng giá trị TS',
        compute='_compute_thong_ke_tai_san_pb',
        store=True
    )
    
    so_tai_san_can_bao_tri = fields.Integer(
        string='TS cần bảo trì',
        compute='_compute_thong_ke_tai_san_pb'
    )
    
    @api.depends('tai_san_phong_ban_ids', 'tai_san_phong_ban_ids.trang_thai', 'tai_san_phong_ban_ids.gia_tri_con_lai')
    def _compute_thong_ke_tai_san_pb(self):
        for record in self:
            record.so_tai_san_phong_ban = len(record.tai_san_phong_ban_ids)
            
            tai_san_dang_su_dung = record.tai_san_phong_ban_ids.filtered(
                lambda ts: ts.trang_thai == 'dang_su_dung'
            )
            record.so_tai_san_dang_su_dung_pb = len(tai_san_dang_su_dung)
            record.tong_gia_tri_tai_san_pb = sum(tai_san_dang_su_dung.mapped('gia_tri_con_lai'))
            
            tai_san_bao_tri = record.tai_san_phong_ban_ids.filtered(
                lambda ts: ts.trang_thai == 'bao_tri'
            )
            record.so_tai_san_can_bao_tri = len(tai_san_bao_tri)
