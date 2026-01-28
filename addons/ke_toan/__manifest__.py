# -*- coding: utf-8 -*-
{
<<<<<<< HEAD
    'name': 'Quản lý Tài chính/Kế toán',
    'version': '15.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Quản lý tài chính kế toán với tự động tính toán',
    'description': """
        Quản lý Tài chính/Kế toán
        ==========================
        - Hệ thống tài khoản kế toán
        - Sổ cái kế toán
        - Tự động ghi nhận khấu hao tài sản
        - Quản lý dòng tiền và ngân sách
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'nhan_su', 'tai_san'],
    'data': [
        'security/ir.model.access.csv',
        'views/tai_khoan_ke_toan_view.xml',
        'views/so_cai_view.xml',
        'views/nhan_su_extend.xml',
        'views/khau_hao_extend.xml',
        'views/menu.xml',
        'data/tai_khoan_ke_toan_data.xml',
    ],
=======
    'name': 'Quản Lý Tài Chính / Kế Toán',
    'version': '15.0.1.0.1',
    'category': 'Accounting/Accounting',
    'summary': 'Quản lý tài chính, kế toán, sổ cái, bút toán',
    'description': """
        Module Quản Lý Tài Chính / Kế Toán
        ===================================
        * Quản lý hệ thống tài khoản kế toán
        * Quản lý sổ cái, bút toán
        * Quản lý kỳ kế toán
        * Tích hợp với module Nhân sự (lương, chấm công)
        * Tích hợp với module Tài sản (khấu hao, thanh lý)
        * Báo cáo tài chính
        * Cấu hình tài khoản kế toán linh hoạt
        
        Version 15.0.1.0.1:
        -------------------
        * Thêm cấu hình tài khoản kế toán mặc định
        * Cải thiện tích hợp với module tài sản (hook pattern)
        * Xóa model dư thừa, tối ưu hiệu suất
        * Migration script tự động
    """,
    'author': 'FIT DNU',
    'website': 'https://fit.dnu.edu.vn',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'nhan_su', 'quan_ly_tai_san'],
    'data': [
        'security/ir.model.access.csv',
        'data/tai_khoan_data.xml',
        'data/sequence_data.xml',
        'data/demo_data.xml',
        'views/tai_khoan_ke_toan_views.xml',
        'views/ky_ke_toan_views.xml',
        'views/so_cai_views.xml',
        'views/but_toan_views.xml',
        'views/bao_cao_views.xml',
        'views/nhan_su_ke_toan_views.xml',
        'views/tai_san_ke_toan_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
>>>>>>> cc63fe88 (update)
    'installable': True,
    'application': True,
    'auto_install': False,
}
