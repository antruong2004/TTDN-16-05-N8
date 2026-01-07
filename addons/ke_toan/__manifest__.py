# -*- coding: utf-8 -*-
{
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
    'installable': True,
    'application': True,
    'auto_install': False,
}
