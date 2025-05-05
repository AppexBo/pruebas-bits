from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    tracking_number = fields.Char(string="Tracking Number")

    # Campo relacionado con account.move (puede ser una factura, por ejemplo)
    account_move = fields.Many2one(
        "account.move",  # Cambia a "res.company" si se refiere a la empresa
        string="Account Move",
    )

    # Ejemplo de un campo relacionado con la empresa
    company_id = fields.Many2one(
        "res.company", 
        string="Company", 
        required=True, 
        default=lambda self: self.env.company
    )
