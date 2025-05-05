from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    
    def write(self, vals):
        if len(self) == 1:
            for field_name in self._fields:
                field_value = getattr(self, field_name, 'No disponible')
                #aqui lo que hago es obtener el campo products_availability_state y valido si dice que esta disponible la cantidad osea que diga available
                if field_name == "products_availability_state" and field_value == "available":  
                    #caso que si haya que automatice a finalizado
                    self.button_validate()
                    #vals["state"] = "done"
        res = super(StockPicking, self).write(vals)
        return res