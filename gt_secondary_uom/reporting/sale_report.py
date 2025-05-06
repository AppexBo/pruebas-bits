# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    secondary_qty = fields.Float(string="Secondary Qty", digits="Product Unit of Measure", groups="gt_secondary_uom.group_sale_secondary_uom")
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["secondary_qty"] = "l.secondary_qty"
        res["secondary_uom"] = "l.secondary_uom"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            l.secondary_qty,l.secondary_uom"""
        return res
