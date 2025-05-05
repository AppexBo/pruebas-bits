from odoo import models, fields

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    # Relación con account.move o res.company según el caso
    account_move = fields.Many2one(
        "account.move",  # Cambia a "res.company" si se refiere a la empresa
        string="Account Move",
        default=lambda self: self.order_id.account_move.id if self.order_id and self.order_id.account_move else None,
    )

    order_id = fields.Many2one(  # Asegúrate de que este campo está definido
        "pos.order", 
        string="Order", 
        required=True,  # Si siempre debe estar relacionado
        ondelete="cascade"
    )
