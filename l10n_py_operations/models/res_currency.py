# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class ResCurrency(models.Model):
    _inherit = ['res.currency']
    
    def get_py_rate(self):
        return round(self.inverse_rate, 2)
        

    def getCode(self):
        if self.l10n_py_currency_id:
            return self.l10n_py_currency_id.code
        raise UserError(f'Moneda: {self.name}, no tiene un codigo PY')
    
    def getdDescription(self):
        if self.l10n_py_currency_id:
            return self.l10n_py_currency_id.description
        raise UserError(f'Moneda: {self.name}, no tiene un codigo PY')
    