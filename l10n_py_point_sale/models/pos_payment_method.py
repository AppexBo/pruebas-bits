# -*- coding:utf-8 -*-

from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)
    

class PosPaymentMethod(models.Model):
    _inherit = ['pos.payment.method']

    l10n_py_payment_type_id = fields.Many2one(
        string='Tipo pago (PY)',
        comodel_name='l10n.py.payment.type',
        help='Tipo de pago paraguay'
    )

    
    card_denomination_id = fields.Many2one(
        string='Denominacion de tarjeta',
        comodel_name='l10n.py.card.denomination'
    )
    
    