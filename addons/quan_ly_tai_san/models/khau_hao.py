# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.models import NewId
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class KhauHao(models.Model):
    _name = 'khau_hao'
    _description = 'Khấu hao tài sản'
    _rec_name = 'ma_khau_hao'
    _order = 'ngay_khau_hao desc'

    ma_khau_hao = fields.Char(string='Mã khấu hao', required=True, copy=False, readonly=True,
                              default=lambda self: self.env['ir.sequence'].next_by_code('khau_hao') or 'New')
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    ngay_khau_hao = fields.Date(string='Ngày khấu hao', required=True, default=fields.Date.context_today)
    thang_khau_hao = fields.Integer(string='Tháng khấu hao', required=True)
    nam_khau_hao = fields.Integer(string='Năm khấu hao', required=True)
    gia_tri_khau_hao = fields.Float(string='Giá trị khấu hao', required=True, default=0.0)
    gia_tri_con_lai = fields.Float(string='Giá trị còn lại', compute='_compute_gia_tri_con_lai', store=True)
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_ghi_nhan', 'Đã ghi nhận'),
        ('huy', 'Đã hủy'),
    ], string='Trạng thái', default='nhap', required=True)
    
    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('tai_san_id.gia_tri_ban_dau', 'gia_tri_khau_hao', 'tai_san_id.tong_khau_hao')
    def _compute_gia_tri_con_lai(self):
        """Tính giá trị còn lại sau khấu hao"""
        for record in self:
            if record.tai_san_id:
                # Nếu là record mới (chưa có ID thật) hoặc đã ghi nhận
                if not record.id or isinstance(record.id, NewId):
                    # Dùng tổng khấu hao từ tài sản
                    record.gia_tri_con_lai = record.tai_san_id.gia_tri_con_lai
                else:
                    # Tính tổng khấu hao đã ghi nhận của tài sản
                    tong_khau_hao = sum(self.search([
                        ('tai_san_id', '=', record.tai_san_id.id),
                        ('trang_thai', '=', 'da_ghi_nhan')
                    ]).mapped('gia_tri_khau_hao'))
                    record.gia_tri_con_lai = record.tai_san_id.gia_tri_ban_dau - tong_khau_hao
            else:
                record.gia_tri_con_lai = 0.0

    @api.model
    def create(self, vals):
        if vals.get('ma_khau_hao', 'New') == 'New':
            vals['ma_khau_hao'] = self.env['ir.sequence'].next_by_code('khau_hao') or 'KH001'
        return super(KhauHao, self).create(vals)

    @api.onchange('ngay_khau_hao')
    def _onchange_ngay_khau_hao(self):
        if self.ngay_khau_hao:
            self.thang_khau_hao = self.ngay_khau_hao.month
            self.nam_khau_hao = self.ngay_khau_hao.year

    def action_ghi_nhan(self):
        """Ghi nhận khấu hao - Gọi hook để module kế toán xử lý"""
        for record in self:
            if record.trang_thai == 'nhap':
                record.trang_thai = 'da_ghi_nhan'
                
                # Hook cho module kế toán tạo bút toán (nếu có)
                if hasattr(record, 'action_tao_but_toan_khau_hao'):
                    record.action_tao_but_toan_khau_hao()
        return True

    def action_huy(self):
        """Hủy khấu hao"""
        for record in self:
            record.trang_thai = 'huy'
            
            # Hook cho module kế toán hủy bút toán (nếu có)
            if hasattr(record, 'action_huy_but_toan_khau_hao'):
                record.action_huy_but_toan_khau_hao()
        return True

    _sql_constraints = [
        ('gia_tri_khau_hao_positive', 'check(gia_tri_khau_hao >= 0)', 'Giá trị khấu hao phải >= 0!')
    ]
    @api.model
    def tinh_gia_tri_khau_hao_thang(self, tai_san):
        """
        Tính giá trị khấu hao của tài sản trong tháng
        
        Args:
            tai_san: record của model tai_san
            
        Returns:
            float: Giá trị khấu hao trong tháng
        """
        if not tai_san.gia_tri_ban_dau or tai_san.gia_tri_ban_dau <= 0:
            return 0.0
            
        if not tai_san.thoi_gian_su_dung or tai_san.thoi_gian_su_dung <= 0:
            return 0.0
        
        # Kiểm tra xem đã khấu hao đủ chưa
        tong_khau_hao = sum(tai_san.khau_hao_ids.filtered(
            lambda x: x.trang_thai == 'da_ghi_nhan'
        ).mapped('gia_tri_khau_hao'))
        
        gia_tri_con_lai = tai_san.gia_tri_ban_dau - tong_khau_hao
        
        if gia_tri_con_lai <= 0:
            return 0.0
        
        # Tính khấu hao theo phương pháp
        if tai_san.phuong_phap_khau_hao == 'duong_thang':
            # Phương pháp đường thẳng: Giá trị / Số tháng
            gia_tri_khau_hao_thang = tai_san.gia_tri_ban_dau / tai_san.thoi_gian_su_dung
            
        elif tai_san.phuong_phap_khau_hao == 'so_du_giam_dan':
            # Phương pháp số dư giảm dần: Giá trị còn lại * tỷ lệ khấu hao
            ty_le_thang = tai_san.ty_le_khau_hao / 100 / 12
            gia_tri_khau_hao_thang = gia_tri_con_lai * ty_le_thang
            
        elif tai_san.phuong_phap_khau_hao == 'tong_so_nam':
            # Phương pháp tổng số năm: (Số tháng còn lại / tổng số tháng) * giá trị ban đầu
            so_thang_da_khau_hao = len(tai_san.khau_hao_ids.filtered(
                lambda x: x.trang_thai == 'da_ghi_nhan'
            ))
            so_thang_con_lai = tai_san.thoi_gian_su_dung - so_thang_da_khau_hao
            if so_thang_con_lai > 0:
                tong_so_thang = sum(range(1, tai_san.thoi_gian_su_dung + 1))
                gia_tri_khau_hao_thang = (so_thang_con_lai / tong_so_thang) * tai_san.gia_tri_ban_dau
            else:
                gia_tri_khau_hao_thang = 0.0
        else:
            # Mặc định dùng đường thẳng
            gia_tri_khau_hao_thang = tai_san.gia_tri_ban_dau / tai_san.thoi_gian_su_dung
        
        # Đảm bảo không khấu hao quá giá trị còn lại
        if gia_tri_khau_hao_thang > gia_tri_con_lai:
            gia_tri_khau_hao_thang = gia_tri_con_lai
            
        return round(gia_tri_khau_hao_thang, 2)

    @api.model
    def tao_khau_hao_tu_dong(self):
        """
        Hàm chạy tự động (cron) để tạo khấu hao cho tất cả tài sản
        Chạy vào ngày cuối tháng
        """
        _logger.info("====== BẮT ĐẦU TÍNH KHẤU HAO TỰ ĐỘNG ======")
        
        # Lấy ngày hiện tại
        today = fields.Date.context_today(self)
        thang_hien_tai = today.month
        nam_hien_tai = today.year
        
        # Tìm tất cả tài sản đang sử dụng và có thể khấu hao
        tai_san_can_khau_hao = self.env['tai_san'].search([
            ('trang_thai', '=', 'dang_su_dung'),
            ('gia_tri_ban_dau', '>', 0),
            ('thoi_gian_su_dung', '>', 0),
            ('ngay_bat_dau_su_dung', '<=', today),
            ('active', '=', True),
        ])
        
        _logger.info(f"Tìm thấy {len(tai_san_can_khau_hao)} tài sản cần khấu hao")
        
        so_khau_hao_tao_moi = 0
        tong_gia_tri_khau_hao = 0.0
        
        for tai_san in tai_san_can_khau_hao:
            try:
                # Kiểm tra xem đã có khấu hao cho tháng này chưa
                khau_hao_da_ton_tai = self.search([
                    ('tai_san_id', '=', tai_san.id),
                    ('thang_khau_hao', '=', thang_hien_tai),
                    ('nam_khau_hao', '=', nam_hien_tai),
                    ('trang_thai', 'in', ['nhap', 'da_ghi_nhan']),
                ], limit=1)
                
                if khau_hao_da_ton_tai:
                    _logger.info(f"Tài sản {tai_san.ma_tai_san} đã có khấu hao tháng {thang_hien_tai}/{nam_hien_tai}")
                    continue
                
                # Tính giá trị khấu hao
                gia_tri_khau_hao = self.tinh_gia_tri_khau_hao_thang(tai_san)
                
                if gia_tri_khau_hao <= 0:
                    _logger.info(f"Tài sản {tai_san.ma_tai_san} không cần khấu hao (giá trị = 0)")
                    continue
                
                # Tạo bản ghi khấu hao
                khau_hao_vals = {
                    'tai_san_id': tai_san.id,
                    'ngay_khau_hao': today,
                    'thang_khau_hao': thang_hien_tai,
                    'nam_khau_hao': nam_hien_tai,
                    'gia_tri_khau_hao': gia_tri_khau_hao,
                    'trang_thai': 'nhap',
                }
                
                khau_hao = self.create(khau_hao_vals)
                
                # Tự động ghi nhận (sẽ gọi hook để module kế toán xử lý)
                khau_hao.action_ghi_nhan()
                
                so_khau_hao_tao_moi += 1
                tong_gia_tri_khau_hao += gia_tri_khau_hao
                
                _logger.info(f"Tạo khấu hao cho {tai_san.ma_tai_san}: {gia_tri_khau_hao:,.0f} VNĐ")
                
            except Exception as e:
                _logger.error(f"Lỗi khi tạo khấu hao cho tài sản {tai_san.ma_tai_san}: {str(e)}")
                continue
        
        _logger.info(f"====== HOÀN THÀNH: Đã tạo {so_khau_hao_tao_moi} bút toán khấu hao, tổng giá trị: {tong_gia_tri_khau_hao:,.0f} VNĐ ======")
        
        return {
            'so_khau_hao': so_khau_hao_tao_moi,
            'tong_gia_tri': tong_gia_tri_khau_hao,
        }

    def action_tinh_lai_khau_hao(self):
        """
        Tính lại giá trị khấu hao cho bút toán nháp
        Dùng khi muốn cập nhật lại giá trị theo tài sản mới
        """
        for record in self:
            if record.trang_thai == 'nhap' and record.tai_san_id:
                gia_tri_moi = self.tinh_gia_tri_khau_hao_thang(record.tai_san_id)
                record.gia_tri_khau_hao = gia_tri_moi
        return True