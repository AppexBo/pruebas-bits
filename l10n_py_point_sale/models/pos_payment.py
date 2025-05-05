# -*- coding:utf-8 -*-

from odoo import api, models, fields

class PosPayment(models.Model):
    _inherit = ['pos.payment']
    
    card = fields.Char(
        string='Tarjeta',
        readonly=True,
        help='Campo comodin, no usado para guardar la tarjeta',
        copy=False
    )
    
    order = fields.Char(
        string='Session',
        copy=False
    )