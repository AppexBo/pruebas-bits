# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class PosConfig(models.Model):
    _inherit = ['pos.config']
    
    
    
    l10n_py_presence_indicator_id = fields.Many2one(
        string='Indicador de presencia (PY)',
        comodel_name='l10n.py.presence.indicator',
        required=True
    )

    operation_type_id = fields.Many2one(
        string='Tipo operacion',
        comodel_name='l10n.py.operation.type',
    )

    
    identification_type_id = fields.Many2one(
        string='Tipo de identificacion',
        comodel_name='l10n_latam.identification.type',
    )
    
    
    
    receiver_nature = fields.Selection(
        string='Naturaleza del receptor',
        selection=[
            ('1', '(1) Contribuyente'), 
            ('2', '(2) No contribuyente')
        ],
    )
    
    
    taxpayer_type = fields.Selection(
        string='Tipo de contribuyente',
        selection=[
            ('1', 'Persona Física'), 
            ('2', 'Persona Jurídica')
        ]
    )

    

    establishment_id = fields.Many2one(
        string='Establecimiento',
        comodel_name='py.establishment',
    )
    
    expedition_point_id = fields.Many2one(
        string='Punto expedicion',
        comodel_name='expedition.point'
    )

    
    def open_ui(self):
        self.validate_payment_method()
        res = super(PosConfig, self).open_ui()
        return res
    
    def validate_payment_method(self):
        for payment_method_id in self.payment_method_ids:
            if not payment_method_id.l10n_py_payment_type_id:
                raise UserError(f'Todos los metodos de pago para este POS deben tener un Tipo de pago (PY), PAGO: {payment_method_id.name}')
        
        payment_method_ids = self.payment_method_ids.filtered( lambda line : line.l10n_py_payment_type_id.code in ['3','4'])
        if len(payment_method_ids)>1:
            raise UserError(f'Solo puede tener un metodo de pago de tipo tarjeta (PY) en POS, se encontraron: {len(payment_method_ids)}, pagos.')
        if not self.l10n_py_presence_indicator_id:
            raise UserError('Establezca un indicador de presencia')
        