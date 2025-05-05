# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import html
class ProductProduct(models.Model):
    
    _inherit = ['product.product']

    def getCode(self):
        if self.default_code:
            return self.default_code
        raise UserError(f"Producto: {self.name}, no tiene un codigo/referencia interna")
    
    def getDescription(self):
        return html.escape(self.name)