# -*- coding:utf-8 -*-

from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = ['res.partner']
    
    
    operation_type_id = fields.Many2one(
        string='Tipo operacion',
        comodel_name='l10n.py.operation.type',
    )
    
    
    receiver_nature = fields.Selection(
        string='Naturaleza del receptor',
        selection=[
            ('1', '(1) Contribuyente'), 
            ('2', '(2) No contribuyente')
        ],
        default='1',
        required=True,
    )
    
    
    taxpayer_type = fields.Selection(
        string='Tipo de contribuyente',
        selection=[
            ('1', 'Persona Física'), 
            ('2', 'Persona Jurídica')
        ],
        copy=False
    )

    
    house_number = fields.Char(
        string='Nro Casa',
        copy=False
    )
    
    
    distrit_id = fields.Many2one(
        string='Distrito',
        comodel_name='res.city',
    )

    locality_id = fields.Many2one(
        string='Cuidad',
        comodel_name='l10n.py.locality',
    )