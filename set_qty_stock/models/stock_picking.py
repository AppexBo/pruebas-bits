import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def update_selected_stock_pickings(self):
        for order in self:
            for element in order.move_ids_without_package:
                #_logger.info(element)
                try:
                    # quantity es la cantidad y la demanda es product_uom_qty
                    element.write({
                        'quantity': element.product_uom_qty  # Asigna el valor de product_uom_qty a quantity
                    })
                except Exception as e:
                    _logger.error(f"Error al actualizar el elemento {element}: {str(e)}")
                    break  
        #log informativo que se actualizo lo seleccionado
        _logger.info("Se actualizaron todos los stocks seleccionados")
        # Recargar la vista
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }