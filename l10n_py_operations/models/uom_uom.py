# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class UomUom(models.Model):
    
    _inherit = ['uom.uom']
    
    def getCode(self):
        if self.l10n_py_uom_id:
            return self.l10n_py_uom_id.code
        raise UserError(f'Medida: {self.name}, no tiene un tipo unidad de medida (PY)')
    
    def getRepresentation(self):
        if self.l10n_py_uom_id:
            return self.l10n_py_uom_id.representation
        raise UserError(f'Medida: {self.name}, no tiene un tipo unidad de medida (PY)')
    
    