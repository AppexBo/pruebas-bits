# -*- coding:utf-8 -*-

from odoo import api, models, fields

class UomUom(models.Model):
    _inherit = ['uom.uom']
    
    
    l10n_py_uom_id = fields.Many2one(
        string='Tipo uom (PY)',
        comodel_name='l10n.py.uom',
        company_dependent=True
    )