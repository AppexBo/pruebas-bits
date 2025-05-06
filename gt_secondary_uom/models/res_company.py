# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    group_purchase_sec_uom = fields.Boolean()
    group_invoice_sec_uom = fields.Boolean()
    group_stock_sec_uom = fields.Boolean()
    group_sale_sec_uom = fields.Boolean()
    print_purchase_sec_uom = fields.Boolean()
    print_invoice_sec_uom = fields.Boolean()
    print_stock_sec_uom = fields.Boolean()
    print_sale_sec_uom = fields.Boolean()
