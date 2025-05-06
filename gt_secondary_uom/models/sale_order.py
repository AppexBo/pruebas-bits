# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    secondary_qty = fields.Float(string="Secondary Qty", compute='_compute_secondary_qty', digits='Product Unit of Measure', readonly=False, store=True)
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM", readonly=True, store=True)

    @api.depends('product_uom', 'product_uom_qty', 'secondary_qty', 'product_id')
    def _compute_secondary_qty(self):
        for line in self:
            line.secondary_uom = line.product_uom
            if (line.product_id.is_secondary_unit and line.product_id.factor and line.product_id.secondary_uom) or (line.product_id.is_secondary_unit and line.product_id.secondary_uom):
                line.secondary_uom = line.product_id.secondary_uom
            if line.product_uom.category_id == line.secondary_uom.category_id:
                line.secondary_qty = line.product_uom._compute_quantity(line.product_uom_qty, line.secondary_uom)
            else:
                convert_uom_qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
                line.secondary_qty = convert_uom_qty * line.product_id.factor

    @api.onchange('product_uom', 'product_uom_qty', 'product_id')
    def _onchange_product_uom(self):
        self.env.context = dict(self.env.context)
        self.env.context.update({'change_secondary_qty': True})

    @api.onchange('secondary_qty')
    def _onchange_uom_qty(self):
        if not self._context.get('change_secondary_qty'):
            if self.product_uom.category_id == self.secondary_uom.category_id:
                self.product_uom_qty = self.secondary_uom._compute_quantity(self.secondary_qty, self.product_uom)
            elif self.product_id.factor or not self.product_id.factor:
                self.product_uom_qty = (self.secondary_qty or 1) / (self.product_id.factor or 0)

    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        res.update({'secondary_uom': self.secondary_uom, 'secondary_qty': self.secondary_qty})
        return res
