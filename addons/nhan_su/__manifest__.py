# -*- coding: utf-8 -*-
{
    'name': 'Quản Lý Nhân Sự',
    'version': '15.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Quản lý nhân viên, phòng ban, chức vụ, chấm công, bảng lương',
    'description': """
Module Quản Lý Nhân Sự
======================

* Quản lý thông tin nhân viên
* Quản lý phòng ban
* Quản lý chức vụ
* Chấm công hàng ngày với check-in/check-out
* Báo cáo chấm công tháng
* Tính lương tự động với phụ cấp và khấu trừ
* Tích hợp với module quản lý tài sản
    """,
    'author': 'FIT DNU',
    'website': 'https://fit.dnu.edu.vn',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/phong_ban_views.xml',
        'views/chuc_vu_views.xml',
        'views/nhan_vien.xml',
<<<<<<< HEAD
        'views/phong_ban.xml',
        'views/chuc_vu.xml',
        'views/lich_su_cong_tac.xml',
        'views/chung_chi.xml',
        'views/cham_cong.xml',
        'views/bang_luong.xml',
=======
        'views/cham_cong_views.xml',
        'views/bang_luong_views.xml',
>>>>>>> cc63fe88 (update)
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
