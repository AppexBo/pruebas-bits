# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_purchase_sec_uom = fields.Boolean(string="Purchase Secondary Uom", related="company_id.group_purchase_sec_uom", implied_group='gt_secondary_uom.group_purchase_secondary_uom', readonly=False)
    group_invoice_sec_uom = fields.Boolean(string="Invoice Secondary Uom", related="company_id.group_invoice_sec_uom", implied_group='gt_secondary_uom.group_invoice_secondary_uom', readonly=False)
    group_stock_sec_uom = fields.Boolean(string="Stock Secondary Uom", related="company_id.group_stock_sec_uom", implied_group='gt_secondary_uom.group_inventory_secondary_uom', readonly=False)
    group_sale_sec_uom = fields.Boolean(string="Sale Secondary Uom", related="company_id.group_sale_sec_uom", implied_group='gt_secondary_uom.group_sale_secondary_uom', readonly=False)
    print_purchase_sec_uom = fields.Boolean(string="Print Purchase Secondary UOM", related="company_id.print_purchase_sec_uom", readonly=False)
    print_invoice_sec_uom = fields.Boolean(string="Print Invoice Secondary UOM", related="company_id.print_invoice_sec_uom", readonly=False)
    print_stock_sec_uom = fields.Boolean(string="Print Stock Secondary UOM", related="company_id.print_stock_sec_uom", readonly=False)
    print_sale_sec_uom = fields.Boolean(string="Print Sale Secondary UOM", related="company_id.print_sale_sec_uom", readonly=False)
