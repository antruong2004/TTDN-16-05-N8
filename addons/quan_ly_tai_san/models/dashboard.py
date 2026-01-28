# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class TaiSanDashboard(models.Model):
    _name = 'tai_san.dashboard'
    _description = 'Dashboard Tài Sản'

    name = fields.Char(string='Tên', default='Dashboard')
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', 
                                   default=lambda self: self.env.company.currency_id)
    
    # Thống kê tổng quan
    tong_tai_san = fields.Integer(string='Tổng số tài sản', compute='_compute_thong_ke')
    tai_san_dang_dung = fields.Integer(string='Đang sử dụng', compute='_compute_thong_ke')
    tai_san_hong = fields.Integer(string='Hỏng', compute='_compute_thong_ke')
    tai_san_thanh_ly = fields.Integer(string='Đã thanh lý', compute='_compute_thong_ke')
    tai_san_moi = fields.Integer(string='Mới', compute='_compute_thong_ke')
    
    # Thống kê giá trị
    tong_gia_tri_ban_dau = fields.Monetary(string='Tổng giá trị ban đầu', compute='_compute_thong_ke', currency_field='currency_id')
    tong_gia_tri_con_lai = fields.Monetary(string='Tổng giá trị còn lại', compute='_compute_thong_ke', currency_field='currency_id')
    tong_khau_hao = fields.Monetary(string='Tổng đã khấu hao', compute='_compute_thong_ke', currency_field='currency_id')
    ty_le_khau_hao_tb = fields.Float(string='Tỷ lệ khấu hao TB (%)', compute='_compute_thong_ke', digits=(5,1))
    ty_le_su_dung = fields.Float(string='Tỷ lệ sử dụng (%)', compute='_compute_thong_ke', digits=(5,1))
    
    # Thời gian sử dụng và bảo hành
    thoi_gian_su_dung_tb = fields.Integer(string='Thời gian sử dụng TB (tháng)', compute='_compute_thong_ke')
    so_ngay_bao_hanh_tb = fields.Integer(string='Số ngày bảo hành TB', compute='_compute_thong_ke')
    thoi_gian_den_thanh_ly_tb = fields.Integer(string='Thời gian đến thanh lý TB (tháng)', compute='_compute_thong_ke')
    
    # Thống kê bảo hành
    con_bao_hanh = fields.Integer(string='Còn bảo hành', compute='_compute_thong_ke')
    sap_het_bao_hanh = fields.Integer(string='Sắp hết BH (30 ngày)', compute='_compute_thong_ke')
    het_bao_hanh = fields.Integer(string='Hết bảo hành', compute='_compute_thong_ke')
    
    # Thống kê tình trạng
    tinh_trang_tot = fields.Integer(string='Tình trạng tốt', compute='_compute_thong_ke')
    tinh_trang_kha = fields.Integer(string='Tình trạng khá', compute='_compute_thong_ke')
    tinh_trang_tb = fields.Integer(string='Tình trạng TB', compute='_compute_thong_ke')
    tinh_trang_kem = fields.Integer(string='Tình trạng kém', compute='_compute_thong_ke')
    tinh_trang_xuong_cap = fields.Integer(string='Xuống cấp', compute='_compute_thong_ke')
    
    # Thống kê hoạt động
    muon_tra_cho_duyet = fields.Integer(string='Mượn/trả chờ duyệt', compute='_compute_hoat_dong')
    thanh_ly_cho_duyet = fields.Integer(string='Thanh lý chờ duyệt', compute='_compute_hoat_dong')
    kiem_ke_dang_thuc_hien = fields.Integer(string='Kiểm kê đang thực hiện', compute='_compute_hoat_dong')
    luan_chuyen_cho_duyet = fields.Integer(string='Luân chuyển chờ duyệt', compute='_compute_hoat_dong')
    
    @api.depends('name')
    def _compute_thong_ke(self):
        TaiSan = self.env['tai_san']
        today = fields.Date.today()
        
        for record in self:
            # Tất cả tài sản
            all_assets = TaiSan.search([])
            active_assets = TaiSan.search([('active', '=', True)])
            
            # Thống kê số lượng theo trạng thái
            record.tong_tai_san = len(all_assets)
            record.tai_san_dang_dung = TaiSan.search_count([('trang_thai', '=', 'dang_su_dung')])
            record.tai_san_hong = TaiSan.search_count([('trang_thai', '=', 'hong')])
            record.tai_san_thanh_ly = TaiSan.search_count([('trang_thai', '=', 'thanh_ly')])
            record.tai_san_moi = TaiSan.search_count([('trang_thai', '=', 'moi')])
            
            # Thống kê giá trị
            record.tong_gia_tri_ban_dau = sum(active_assets.mapped('gia_tri_ban_dau'))
            record.tong_gia_tri_con_lai = sum(active_assets.mapped('gia_tri_con_lai'))
            record.tong_khau_hao = sum(active_assets.mapped('tong_khau_hao'))
            
            if record.tong_gia_tri_ban_dau > 0:
                record.ty_le_khau_hao_tb = (record.tong_khau_hao / record.tong_gia_tri_ban_dau) * 100
            else:
                record.ty_le_khau_hao_tb = 0
            
            # Tỷ lệ sử dụng
            if record.tong_tai_san > 0:
                record.ty_le_su_dung = (record.tai_san_dang_dung / record.tong_tai_san) * 100
            else:
                record.ty_le_su_dung = 0
            
            # Thời gian sử dụng trung bình (tháng)
            total_months = 0
            count = 0
            for asset in active_assets:
                if asset.ngay_mua:
                    months_used = relativedelta(today, asset.ngay_mua).months + \
                                  (relativedelta(today, asset.ngay_mua).years * 12)
                    total_months += months_used
                    count += 1
            record.thoi_gian_su_dung_tb = int(total_months / count) if count > 0 else 0
            
            # Số ngày bảo hành trung bình
            total_warranty_days = 0
            warranty_count = 0
            for asset in active_assets:
                if asset.ngay_het_bao_hanh and asset.ngay_mua:
                    warranty_days = (asset.ngay_het_bao_hanh - asset.ngay_mua).days
                    total_warranty_days += warranty_days
                    warranty_count += 1
            record.so_ngay_bao_hanh_tb = int(total_warranty_days / warranty_count) if warranty_count > 0 else 0
            
            # Thời gian đến thanh lý TB (giả sử tuổi thọ trung bình là 60 tháng)
            record.thoi_gian_den_thanh_ly_tb = max(0, 60 - record.thoi_gian_su_dung_tb)
            
            # Thống kê bảo hành
            record.con_bao_hanh = TaiSan.search_count([
                ('ngay_het_bao_hanh', '>=', today),
                ('trang_thai', '!=', 'thanh_ly')
            ])
            
            ngay_30_ngay_sau = today + timedelta(days=30)
            record.sap_het_bao_hanh = TaiSan.search_count([
                ('ngay_het_bao_hanh', '>=', today),
                ('ngay_het_bao_hanh', '<=', ngay_30_ngay_sau),
                ('trang_thai', '!=', 'thanh_ly')
            ])
            
            record.het_bao_hanh = TaiSan.search_count([
                ('ngay_het_bao_hanh', '<', today),
                ('trang_thai', '!=', 'thanh_ly')
            ])
            
            # Thống kê tình trạng
            record.tinh_trang_tot = TaiSan.search_count([('muc_do_su_dung', '=', 'tot')])
            record.tinh_trang_kha = TaiSan.search_count([('muc_do_su_dung', '=', 'kha')])
            record.tinh_trang_tb = TaiSan.search_count([('muc_do_su_dung', '=', 'trung_binh')])
            record.tinh_trang_kem = TaiSan.search_count([('muc_do_su_dung', '=', 'kem')])
            record.tinh_trang_xuong_cap = TaiSan.search_count([('muc_do_su_dung', '=', 'xuong_cap')])
    
    @api.depends('name')
    def _compute_hoat_dong(self):
        for record in self:
            # Mượn/trả chờ duyệt
            if 'muon_tra_tai_san' in self.env:
                record.muon_tra_cho_duyet = self.env['muon_tra_tai_san'].search_count([
                    ('trang_thai', '=', 'cho_duyet')
                ])
            else:
                record.muon_tra_cho_duyet = 0
            
            # Thanh lý chờ duyệt
            if 'thanh_ly_tai_san' in self.env:
                record.thanh_ly_cho_duyet = self.env['thanh_ly_tai_san'].search_count([
                    ('trang_thai', '=', 'cho_duyet')
                ])
            else:
                record.thanh_ly_cho_duyet = 0
            
            # Kiểm kê đang thực hiện
            if 'kiem_ke_tai_san' in self.env:
                record.kiem_ke_dang_thuc_hien = self.env['kiem_ke_tai_san'].search_count([
                    ('trang_thai', '=', 'dang_thuc_hien')
                ])
            else:
                record.kiem_ke_dang_thuc_hien = 0
            
            # Luân chuyển chờ duyệt
            if 'luan_chuyen_tai_san' in self.env:
                record.luan_chuyen_cho_duyet = self.env['luan_chuyen_tai_san'].search_count([
                    ('trang_thai', '=', 'cho_duyet')
                ])
            else:
                record.luan_chuyen_cho_duyet = 0
    
    # Actions để điều hướng
    def action_view_tai_san_dang_dung(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tài sản đang sử dụng',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'domain': [('trang_thai', '=', 'dang_su_dung')],
            'context': {'default_trang_thai': 'dang_su_dung'}
        }
    
    def action_view_tai_san_hong(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tài sản hỏng',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'domain': [('trang_thai', '=', 'hong')],
        }
    
    def action_view_con_bao_hanh(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tài sản còn bảo hành',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'domain': [('con_bao_hanh', '=', True)],
        }
    
    def action_view_sap_het_bao_hanh(self):
        today = fields.Date.today()
        ngay_30_ngay_sau = today + timedelta(days=30)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sắp hết bảo hành (30 ngày)',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'domain': [
                ('ngay_het_bao_hanh', '>=', today),
                ('ngay_het_bao_hanh', '<=', ngay_30_ngay_sau)
            ],
        }
    
    def action_view_tinh_trang_kem(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tài sản tình trạng kém',
            'res_model': 'tai_san',
            'view_mode': 'tree,form',
            'domain': [('muc_do_su_dung', 'in', ['kem', 'xuong_cap'])],
        }
    
    def action_view_muon_tra_cho_duyet(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mượn/Trả chờ duyệt',
            'res_model': 'muon_tra_tai_san',
            'view_mode': 'tree,form',
            'domain': [('trang_thai', '=', 'cho_duyet')],
        }
    
    def action_view_thanh_ly_cho_duyet(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Thanh lý chờ duyệt',
            'res_model': 'thanh_ly_tai_san',
            'view_mode': 'tree,form',
            'domain': [('trang_thai', '=', 'cho_duyet')],
        }


class TaiSanThongKeTheoLoai(models.Model):
    """Model phụ trợ cho biểu đồ thống kê theo loại"""
    _name = 'tai_san.thong_ke_loai'
    _description = 'Thống kê tài sản theo loại'
    _auto = False
    _order = 'so_luong desc'
    
    danh_muc_id = fields.Many2one('danh_muc_tai_san', string='Danh mục', readonly=True)
    so_luong = fields.Integer(string='Số lượng', readonly=True)
    tong_gia_tri = fields.Float(string='Tổng giá trị', readonly=True)
    gia_tri_con_lai = fields.Float(string='Giá trị còn lại', readonly=True)
    
    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS tai_san_thong_ke_loai;
            CREATE OR REPLACE VIEW tai_san_thong_ke_loai AS (
                SELECT
                    row_number() OVER () as id,
                    danh_muc_id,
                    COUNT(*) as so_luong,
                    COALESCE(SUM(gia_tri_ban_dau), 0) as tong_gia_tri,
                    COALESCE(SUM(gia_tri_con_lai), 0) as gia_tri_con_lai
                FROM tai_san
                WHERE active = True
                GROUP BY danh_muc_id
            )
        """)


class TaiSanThongKeTheoPhongBan(models.Model):
    """Model phụ trợ cho biểu đồ thống kê theo phòng ban"""
    _name = 'tai_san.thong_ke_phong_ban'
    _description = 'Thống kê tài sản theo phòng ban'
    _auto = False
    _order = 'so_luong desc'
    
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', readonly=True)
    so_luong = fields.Integer(string='Số lượng', readonly=True)
    tong_gia_tri = fields.Float(string='Tổng giá trị', readonly=True)
    
    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS tai_san_thong_ke_phong_ban;
            CREATE OR REPLACE VIEW tai_san_thong_ke_phong_ban AS (
                SELECT
                    row_number() OVER () as id,
                    phong_ban_id,
                    COUNT(*) as so_luong,
                    COALESCE(SUM(gia_tri_ban_dau), 0) as tong_gia_tri
                FROM tai_san
                WHERE active = True AND phong_ban_id IS NOT NULL
                GROUP BY phong_ban_id
            )
        """)


class TaiSanThongKeTheoTrangThai(models.Model):
    """Model phụ trợ cho biểu đồ thống kê theo trạng thái"""
    _name = 'tai_san.thong_ke_trang_thai'
    _description = 'Thống kê tài sản theo trạng thái'
    _auto = False
    
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('hong', 'Hỏng'),
        ('thanh_ly', 'Đã thanh lý')
    ], string='Trạng thái', readonly=True)
    so_luong = fields.Integer(string='Số lượng', readonly=True)
    tong_gia_tri = fields.Float(string='Tổng giá trị', readonly=True)
    
    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS tai_san_thong_ke_trang_thai;
            CREATE OR REPLACE VIEW tai_san_thong_ke_trang_thai AS (
                SELECT
                    row_number() OVER () as id,
                    trang_thai,
                    COUNT(*) as so_luong,
                    COALESCE(SUM(gia_tri_ban_dau), 0) as tong_gia_tri
                FROM tai_san
                GROUP BY trang_thai
            )
        """)
