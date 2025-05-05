# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)



class PosOrder(models.Model):
    _inherit = ['pos.order']

    @api.model
    def set_l10n_py_card(self, _order_id):
        if _order_id:
            order_id = self.browse(_order_id)
            if order_id:
                pos_reference = order_id.pos_reference
                l10n_py_card_id = self.env['l10n.py.card'].search([('name','=',pos_reference)])
                
                if l10n_py_card_id:
                    _logger.info('se encontro una tarjeta')
            
                    return l10n_py_card_id.card
        return False

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        res : dict = super(PosOrder, self)._payment_fields(order,ui_paymentline)
        payment_method_id = res.get('payment_method_id', False)
        if payment_method_id:
            payment_method_id = self.env['pos.payment.method'].browse(payment_method_id)
            if payment_method_id and payment_method_id.l10n_py_payment_type_id and payment_method_id.l10n_py_payment_type_id.code in ['3','4']:
                res['card'] = self.set_l10n_py_card(res.get('pos_order_id',False))
                if payment_method_id.card_denomination_id:
                    res['card_type'] = payment_method_id.card_denomination_id.description
                
        return res
    
    def get_py_payments_type(self):
        if self.payment_ids:
            list_payment = []
            for payment in self.payment_ids:
                list_payment.append(
                    (
                        0, 
                        0, {
                            'l10n_py_payment_type_id': payment.payment_method_id.l10n_py_payment_type_id.id, 
                            'currency_id' : payment.currency_id.id,
                            'amount': payment.amount,
                            'card' : payment.card,
                            'card_denomination_id' : payment.payment_method_id.card_denomination_id.id if payment.payment_method_id.card_denomination_id else False,
                            
                        }
                    )
                )
            return list_payment
        raise UserError('No se encontro un tipo de pago (PY)')
        
    def _prepare_invoice_vals(self):
        vals = super(PosOrder, self)._prepare_invoice_vals()
        if self.config_id.l10n_py_presence_indicator_id:
            vals['l10n_py_presence_indicator_id'] = self.config_id.l10n_py_presence_indicator_id.id
        else:
            raise UserError('No se encontro una configuracion para el tipo de presencia clientes en punto de venta.')
        vals['l10n_py_payments_ids'] = self.get_py_payments_type()
        
        vals['establishment_id'] = self.config_id.establishment_id.id
        vals['expedition_point_id'] = self.config_id.expedition_point_id.id
        
            
        return vals