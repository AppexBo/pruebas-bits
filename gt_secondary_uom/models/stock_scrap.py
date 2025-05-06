# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    secondary_qty = fields.Float(string="Secondary Qty", compute='_compute_secondary_qty', digits='Product Unit of Measure', readonly=False)
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM", readonly=True)

    @api.depends('product_uom_id', 'scrap_qty', 'product_id')
    def _compute_secondary_qty(self):
        for line in self:
            line.secondary_uom = line.product_uom_id
            line.env.context = dict(line.env.context)
            line.env.context.update({'change_secondary_qty': True})
            if line.product_id.is_secondary_unit and line.product_id.secondary_uom:
                line.secondary_uom = line.product_id.secondary_uom
            if line.product_uom_id.category_id == line.secondary_uom.category_id:
                line.secondary_qty = line.product_uom_id._compute_quantity(line.scrap_qty, line.secondary_uom)
            else:
                convert_uom_qty = line.product_uom_id._compute_quantity(line.scrap_qty, line.product_id.uom_id)
                line.secondary_qty = convert_uom_qty * line.product_id.factor

    @api.onchange('secondary_qty')
    def _onchange_uom_qty(self):
        if not self._context.get('change_secondary_qty'):
            if self.product_uom_id.category_id == self.secondary_uom.category_id:
                self.scrap_qty = self.secondary_uom._compute_quantity(self.secondary_qty, self.product_uom_id)
            elif self.product_id.factor:
                self.scrap_qty = (self.secondary_qty or 1) / (self.product_id.factor or 0)
