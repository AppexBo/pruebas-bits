# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.float_utils import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    secondary_done = fields.Float(string="Secondary Done Qty", compute="_compute_secondary_done_qty", digits="Product Unit of Measure", readonly=False, store=True)
    secondary_qty = fields.Float(string="Secondary Qty", compute="_compute_secondary_qty", digits="Product Unit of Measure", states={'done': [('readonly', True)]}, store=True)
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM", readonly=True, store=True)

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        res.update({
            'secondary_qty': self.secondary_qty,
            'secondary_uom': self.secondary_uom.id
        })
        return res

    def manage_secondary_uom(self):
        self.ensure_one()
        self.secondary_uom = self.product_uom
        self.env.context = dict(self.env.context)
        self.env.context.update({'change_secondary_qty': True})
        if (self.product_id.is_secondary_unit and self.product_id.factor and self.product_id.secondary_uom) or (self.product_id.is_secondary_unit and self.product_id.secondary_uom):
            self.secondary_uom = self.product_id.secondary_uom

    @api.depends("product_uom_qty", "secondary_qty", "product_uom")
    def _compute_secondary_qty(self):
        for line in self:
            line.manage_secondary_uom()
            if line.product_uom.category_id == line.secondary_uom.category_id:
                line.secondary_qty = line.product_uom._compute_quantity(line.product_uom_qty, line.secondary_uom)
            else:
                convert_uom_qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
                line.secondary_qty = convert_uom_qty * line.product_id.factor

    @api.onchange('secondary_qty')
    def _onchange_secondary_uom_qty(self):
        if not self._context.get('change_secondary_qty'):
            if self.product_uom.category_id == self.secondary_uom.category_id:
                self.product_uom_qty = self.secondary_uom._compute_quantity(self.secondary_qty, self.product_uom)
            elif self.product_id.factor:
                self.product_uom_qty = (self.secondary_qty or 1) / (self.product_id.factor or 0)

    @api.depends("quantity", "secondary_done")
    def _compute_secondary_done_qty(self):
        for line in self:
            line.manage_secondary_uom()
            if line.product_uom.category_id == line.secondary_uom.category_id:
                line.secondary_done = line.product_uom._compute_quantity(line.quantity, line.secondary_uom)
            else:
                convert_uom_qty = line.product_uom._compute_quantity(line.quantity, line.product_id.uom_id)
                line.secondary_done = convert_uom_qty * line.product_id.factor

    @api.onchange('product_uom', 'quantity', 'product_id')
    def _onchange_product_uom_qty(self):
        self.env.context = dict(self.env.context)
        self.env.context.update({'change_secondary_qty': True})

    @api.onchange('secondary_done')
    def _onchange_secondary_done_qty(self):
        if not self._context.get('change_secondary_qty'):
            if self.product_uom.category_id == self.secondary_uom.category_id:
                self.quantity = self.secondary_uom._compute_quantity(self.secondary_done, self.product_uom)
            elif self.product_id.factor:
                self.quantity = (self.secondary_done or 1) / (self.product_id.factor or 0)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    secondary_qty = fields.Float(string="Secondary Qty", digits="Product Unit of Measure", readonly=True, store=True)
    secondary_done = fields.Float(string="Secondary Qty Done", compute="_compute_sec_done_qty", readonly=False, store=True)
    secondary_uom = fields.Many2one(related="move_id.secondary_uom", string="Secondary UOM", readonly=True, store=True)

    @api.depends("quantity", "secondary_done")
    def _compute_sec_done_qty(self):
        for line in self:
            line.secondary_done = line.move_id.secondary_qty
            line.secondary_uom = line.move_id.secondary_uom.id
            line.env.context = dict(line.env.context)
            line.env.context.update({'change_secondary_qty': True})
            if line.product_uom_id.category_id == line.secondary_uom.category_id:
                line.secondary_done = line.product_uom_id._compute_quantity(line.quantity, line.secondary_uom)
            else:
                convert_uom_qty = line.product_uom_id._compute_quantity(line.quantity, line.product_uom_id)
                line.secondary_done = (convert_uom_qty * line.move_id.product_id.factor)

    @api.onchange("secondary_done")
    def _onchange_qty(self):
        for line in self:
            if not self._context.get('change_secondary_qty'):
                if line.product_uom_id.category_id == line.secondary_uom.category_id:
                    line.quantity = line.secondary_uom._compute_quantity(line.secondary_done, line.product_uom_id)
                elif line.move_id.product_id.factor:
                    line.quantity = (line.secondary_done or 1) / (line.move_id.product_id.factor or 0)

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = {}

        def get_aggregated_properties(move_line=False, move=False):
            move = move or move_line.move_id
            uom = move.product_uom or move_line.product_uom_id
            name = move.product_id.display_name
            description = move.description_picking
            secondary_uom = move.secondary_uom
            secondary_done = move.secondary_done
            secondary_qty = move.secondary_qty
            if description == name or description == move.product_id.name:
                description = False
            product = move.product_id
            line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}_{move.product_packaging_id or ""}'
            return (line_key, name, description, uom, move.product_packaging_id, secondary_uom, secondary_done, secondary_qty)

        def _compute_packaging_qtys(aggregated_move_lines):
            # Needs to be computed after aggregation of line qtys
            for line in aggregated_move_lines.values():
                if line['packaging']:
                    line['packaging_qty'] = line['packaging']._compute_qty(line['qty_ordered'], line['product_uom'])
                    line['packaging_quantity'] = line['packaging']._compute_qty(line['quantity'], line['product_uom'])
            return aggregated_move_lines

        backorders = self.env["stock.picking"]
        pickings = self.picking_id
        while pickings.backorder_ids:
            backorders |= pickings.backorder_ids
            pickings = pickings.backorder_ids

        for move_line in self:
            if kwargs.get("except_package") and move_line.result_package_id:
                continue
            line_key, name, description, uom, packaging, secondary_uom, secondary_done, secondary_qty = get_aggregated_properties(move_line=move_line)
            secondary_done = secondary_done
            secondary_qty = secondary_qty
            quantity = move_line.product_uom_id._compute_quantity(move_line.quantity, uom)
            if line_key not in aggregated_move_lines:
                qty_ordered = None
                if backorders and not kwargs.get("strict"):
                    qty_ordered = move_line.move_id.product_uom_qty
                    secondary_qty = move_line.move_id.secondary_qty
                    following_move_lines = backorders.move_line_ids.filtered(
                        lambda ml: get_aggregated_properties(move=ml.move_id)[0] == line_key)
                    qty_ordered += sum(following_move_lines.move_id.mapped("product_uom_qty"))
                    previous_move_lines = move_line.move_id.move_line_ids.filtered(
                        lambda ml: get_aggregated_properties(move=ml.move_id)[0] == line_key and ml.id != move_line.id)
                    qty_ordered -= sum([m.product_uom_id._compute_quantity(m.quantity, uom) for m in previous_move_lines])
                aggregated_move_lines[line_key] = {
                    "name": name,
                    "description": description,
                    "quantity": quantity,
                    "qty_ordered": qty_ordered or quantity,
                    "product_uom": uom,
                    'packaging': packaging,
                    "secondary_done": secondary_done,
                    "secondary_qty": secondary_qty,
                    "secondary_uom": secondary_uom,
                    "product": move_line.product_id,
                }
            else:
                aggregated_move_lines[line_key]["qty_ordered"] += quantity
                aggregated_move_lines[line_key]["quantity"] += quantity

        if kwargs.get("strict"):
            # return aggregated_move_lines
            return _compute_packaging_qtys(aggregated_move_lines)
        pickings = (self.picking_id | backorders)
        for empty_move in pickings.move_ids:
            if not (
                empty_move.state == "cancel"
                and empty_move.product_uom_qty
                and float_is_zero(empty_move.quantity, precision_rounding=empty_move.product_uom.rounding)
            ):
                continue
            line_key, name, description, uom, packaging, secondary_uom, secondary_done, secondary_qty = get_aggregated_properties(move=empty_move)

            if line_key not in aggregated_move_lines:
                qty_ordered = empty_move.product_uom_qty
                aggregated_move_lines[line_key] = {
                    "name": name,
                    "description": description,
                    "quantity": False,
                    "qty_ordered": qty_ordered,
                    "product_uom": uom,
                    "secondary_done": secondary_done,
                    "secondary_qty": secondary_qty,
                    "secondary_uom": secondary_uom,
                    "product": empty_move.product_id,
                    'packaging': packaging,
                }
            else:
                aggregated_move_lines[line_key]["qty_ordered"] += empty_move.product_uom_qty
                aggregated_move_lines[line_key]["secondary_qty"] += empty_move.secondary_qty

        return aggregated_move_lines


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        if values.get("secondary_uom"):
            move_values.update({
                'secondary_uom': values["secondary_uom"].id,
                'secondary_qty': values["secondary_qty"]
            })
        return move_values


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    secondary_qty = fields.Float(string="Secondary Qty", compute='_compute_secondary_qty', digits='Product Unit of Measure', readonly=False, store=True)
    secondary_uom = fields.Many2one("uom.uom", string="Secondary UOM", readonly=True, store=True)

    @api.depends('quantity', 'product_uom_id', 'product_id')
    def _compute_secondary_qty(self):
        for line in self:
            line.secondary_uom = line.product_uom_id
            if (line.product_id.is_secondary_unit and line.product_id.factor and line.product_id.secondary_uom) or (line.product_id.is_secondary_unit and line.product_id.secondary_uom):
                line.secondary_uom = line.product_id.secondary_uom
            if line.product_uom_id.category_id == line.secondary_uom.category_id:
                line.secondary_qty = line.product_uom_id._compute_quantity(line.quantity, line.secondary_uom)
            else:
                convert_uom_qty = line.product_uom_id._compute_quantity(line.quantity, line.product_id.uom_id)
                line.secondary_qty = convert_uom_qty * line.product_id.factor

    @api.onchange('product_uom_id', 'quantity')
    def _onchange_product_uom(self):
        self.env.context = dict(self.env.context)
        self.env.context.update({'change_secondary_qty': True})

    @api.onchange('secondary_qty')
    def _onchange_uom_qty(self):
        if not self._context.get('change_secondary_qty'):
            if self.product_uom_id.category_id == self.secondary_uom.category_id:
                self.inventory_quantity = self.secondary_uom._compute_quantity(self.secondary_qty, self.product_uom_id)
            elif self.product_id.factor or not self.product_id.factor:
                self.inventory_quantity = (self.secondary_qty or 1) / (self.product_id.factor or 0)
            self.action_apply_inventory()
