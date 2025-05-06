# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    secondary_qty = fields.Float(string="Secondary Qty", digits='Product Unit of Measure', groups="gt_secondary_uom.group_invoice_secondary_uom")
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM")

    def _select(self):
        return super()._select() + ", line.secondary_qty as secondary_qty" + ", line.secondary_uom as secondary_uom"
