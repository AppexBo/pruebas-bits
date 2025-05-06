# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM")
    is_secondary_unit = fields.Boolean(string="Is Secondary Unit?")
    factor = fields.Float(string="Ratio")
    uom_match = fields.Boolean()

    @api.onchange("secondary_uom", "uom_id", "is_secondary_unit")
    def onchange_uom(self):
        self.uom_match = self.is_secondary_unit and self.secondary_uom.category_id == self.uom_id.category_id
        if not self.is_secondary_unit:
            self.secondary_uom = False
            self.factor = 0
