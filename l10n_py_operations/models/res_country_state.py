# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class ResCountry(models.Model):
    _inherit = ['res.country']

    def get_country_info(self):
        if self.l10n_py_country_id:
            return self.l10n_py_country_id.get_country_info()
        raise UserError(f"Pais: {self.name}, no tien un tipo pais (PY)")
    

class ResCountryState(models.Model):
    
    _inherit = ['res.country.state']
    
    def get_department_info(self):
        return self.code, self.name
    
class ResCity(models.Model):
    _inherit = ['res.city']
    
    def get_department_distrit_info(self):
        return self.code, self.name
    

class L10nPyLocality(models.Model):
    
    _inherit = ['l10n.py.locality']
    
    def get_department_distrit_city_info(self):
        return self.code, self.description