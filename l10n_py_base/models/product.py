# -*- coding: utf-8 -*-

from odoo import api, models, fields
from html import escape
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    
    _inherit = ['product.product']
    
    def get_product_tag_ids_description(self, required = False):
        tags_description = ''
        if self.product_tag_ids:
            for product_tag_id in self.product_tag_ids:
                tags_description += escape(product_tag_id.name)
        
        if required and not tags_description:
            raise UserError(f"No se encotro etiquetas en la plantilla de producto: {self.name}, Las etiquetas serviran de informacion de interes de Fisco respecto al DE, segun el Art. 3 Inc. 7 de la resolucion general Nro. 41/2014")
        return tags_description