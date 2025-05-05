# -*- coding:utf-8 -*-

from odoo import api, models, fields

class L10nPyCountry(models.Model):
    _inherit = ['l10n.py.country']
    
    def get_country_info(self):
        return self.representation, self.description
    