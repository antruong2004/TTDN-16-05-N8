# -*- coding: utf-8 -*-
{
    'name': 'Quản lý Tài sản',
    'version': '15.0.1.0.0',
    'category': 'Asset Management',
    'summary': 'Quản lý tài sản và khấu hao tự động',
    'description': """
        Quản lý Tài sản
        ================
        - Quản lý thông tin tài sản
        - Phân loại tài sản
        - Tính toán khấu hao tự động hàng tháng
        - Ghi nhận vào sổ cái kế toán
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/loai_tai_san_view.xml',
        'views/tai_san_view.xml',
        'views/khau_hao_view.xml',
        'views/nhan_su_extend.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
