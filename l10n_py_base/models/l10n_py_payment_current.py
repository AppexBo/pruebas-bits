# -*- coding:utf-8 -*-

from odoo import api,models, fields

class L10nPyPaymentCurrent(models.Model):
    _name = "l10n.py.payment.currency"
    _description = 'Monto y moneda de tipo de pago'

    
    l10n_py_payment_type_id = fields.Many2one(
        string='Tipo de pago (PY)',
        comodel_name='l10n.py.payment.type',
        
        required=True
        
    )
    
    
    currency_id = fields.Many2one(
        string='Moneda',
        comodel_name='res.currency',
        required=True,
        
        default= lambda self : self.get_default_currency_id()
    )
    
    def get_default_currency_id(self):
        currency_id = self.env.ref('base.PYG')
        return currency_id.id
    
    amount = fields.Float(
        string='Monto pagado',
        digits=(16, 4)
    )
    
    
    card = fields.Char(
        string='Numero tarjeta',
        size=4
    )
    
    
    currency_rate = fields.Float(
        string='Tipo de cambio',
    )
    
    
    invoice_id = fields.Many2one(
        string='Factura',
        comodel_name='account.move',
    )
    
    
    card_denomination_id = fields.Many2one(
        string='Denominacion de tarjeta',
        comodel_name='l10n.py.card.denomination'
    )
    