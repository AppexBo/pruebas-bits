# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']
    
    
    taxes_percentage_type = fields.Selection(
        string="Tipo (%) tasa",
        selection=[
            ('0', 'Gravado 0%'), 
            ('5', 'Gravado 5%'), 
            ('10', 'Gravado 10%')
        ],
        default='0',
        help='Corresponde al porcentaje (%) de la tasa'
    )
    

    def get_E734(self):
        if self.move_type == 'in_invoice':
            return int(self.taxes_percentage_type)
        else:
            return super(AccountMoveLine, self).get_E734()