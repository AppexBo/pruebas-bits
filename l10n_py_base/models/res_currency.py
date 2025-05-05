# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class ResCurrency(models.Model):
    _inherit = ['res.currency']
    
    
    l10n_py_currency_id = fields.Many2one(
        string='Tipo moneda (PY)',
        comodel_name='l10n.py.currency',
        company_dependent=True
    )
    
    