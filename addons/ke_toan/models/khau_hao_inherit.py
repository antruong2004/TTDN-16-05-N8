# -*- coding: utf-8 -*-

from odoo import models, fields


class KhauHaoInherit(models.Model):
    _inherit = 'khau_hao'

    so_cai_id = fields.Many2one(
        comodel_name='so_cai',
        string="Sổ cái",
        ondelete='set null',
        help="Bút toán kế toán được tạo tự động"
    )
