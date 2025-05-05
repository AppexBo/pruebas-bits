# -*- coding:utf-8 -*-

from odoo import api, models, fields

class L10nPyCard(models.Model):
    _name = 'l10n.py.card'
    _description = 'Tarjeta de venta'

    
    name = fields.Char(
        string='Session',
        required=True
    )
    
    
    card = fields.Char(
        string='Nro. Tarjeta',
        required=True
    )
    
    
    company_id = fields.Many2one(
        string='Compañia', 
        comodel_name='res.company', 
        required=True, 
        default=lambda self: self.env.company
    )
    