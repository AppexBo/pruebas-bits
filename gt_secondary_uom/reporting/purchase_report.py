# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    secondary_qty = fields.Float(string="Secondary Qty", digits="Product Unit of Measure", groups="gt_secondary_uom.group_purchase_secondary_uom")
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM")

    def _select(self):
        return (super()._select() + ", l.secondary_qty as secondary_qty" + ", l.secondary_uom as secondary_uom")

    def _group_by(self):
        res = super()._group_by()
        res += """, l.secondary_qty,l.secondary_uom"""
        return res
