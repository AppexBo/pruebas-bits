# -*- coding:utf-8 -*-

from odoo import api, models, fields

class ResCountry(models.Model):
    _inherit = ['res.country']
    

    
    l10n_py_country_id = fields.Many2one(
        string='Codigo tipo pais',
        comodel_name='l10n.py.country'
    )
    