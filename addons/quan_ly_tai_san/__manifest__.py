# -*- coding: utf-8 -*-
{
    'name': 'Quản Lý Tài Sản',
    'version': '15.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Quản lý tài sản cố định, khấu hao, thanh lý, kiểm kê',
    'description': """
        Module Quản Lý Tài Sản
        =======================
        * Quản lý danh mục tài sản cố định
        * Tính khấu hao tự động theo các phương pháp
        * Phân bổ tài sản theo phòng ban/nhân viên
        * Mượn/trả tài sản
        * Thanh lý tài sản
        * Kiểm kê tài sản định kỳ
        * Luân chuyển tài sản
        * Tích hợp kế toán
    """,
    'author': 'FIT DNU',
    'website': 'https://fit.dnu.edu.vn',
    'license': 'LGPL-3',
    'depends': ['base', 'nhan_su', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/dashboard_data.xml',
        'data/cron_khau_hao.xml',
        'views/danh_muc_tai_san_views.xml',
        'views/tai_san_views.xml',
        'views/lich_su_bao_tri_views.xml',
        'views/khau_hao_views.xml',
        'views/phan_bo_tai_san_views.xml',
        'views/muon_tra_tai_san_views.xml',
        'views/thanh_ly_tai_san_views.xml',
        'views/kiem_ke_tai_san_views.xml',
        'views/luan_chuyen_tai_san_views.xml',
        'views/dashboard_simple.xml',
        'views/nhan_su_extend_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
