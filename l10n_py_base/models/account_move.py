# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = ['account.move']

    operacion_condition_dict = {
        '1' : 'Contado',
        '2' : 'Crédito'
    }

    
    country_partner_id = fields.Many2one(
        string='Pais',
        comodel_name='res.country',
        related='partner_id.country_id',
        readonly=True,
        store=True
    )
    
    
    
    l10n_py_invoice_sign_date = fields.Datetime(
        string='Fecha firmado (PY)'
    )

    
    l10n_py_ringing_date = fields.Date(
        string='Fecha inicio vigencia timbrado (PY)',
    )

    
    l10n_py_emision_date = fields.Datetime(
        string='Fecha emision factura (PY)',
    )
    
    
    
    l10n_py_payment_type_id = fields.Many2one(
        string='Tipo pago (PY)',
        comodel_name='l10n.py.payment.type'
    )

    
    l10n_py_payments_ids = fields.One2many(
        string='Metodos de pago (PY)',
        comodel_name='l10n.py.payment.currency',
        inverse_name='invoice_id',
    )
    

    l10n_py_transaction_type_id = fields.Many2one(
        string='Tipo transacccion',
        comodel_name='l10n.py.transaction.type',
        default= lambda self : self.env.ref('l10n_py_base.l10n_py_transaction_type_1')
    )

    l10n_py_tax_affectation_type = fields.Many2one(
        string='Tipo de impuesto afectado',
        comodel_name='l10n.py.tax.affectation.type',
        default= lambda self : self.env.ref('l10n_py_base.l10n_py_affectation_1'), 
        raise_if_not_found=False
    )

    
    l10n_py_presence_indicator_id = fields.Many2one(
        string='Indicador de presencia',
        comodel_name='l10n.py.presence.indicator',
    )
    
    
    xml_str_format = fields.Text(
        string='Formato XML str',
        copy=False
    )
    
    
    py_file_content = fields.Binary(
        string='Archivo base64 (PY)',
        copy=False
        
    )

    
    format_base64_xml = fields.Text(
        string='Formato str base64',
        copy=False
    )
    
    
    l10n_py_transaction = fields.Boolean(
        string='Transaccion (PY)',
        default=True
    )

    
    l10n_py_response = fields.Text(
        string='l10n_py_response',
        copy=False
    )
    
    
    
    l10n_py_response_Success = fields.Boolean(
        string='Success',
        copy=False
    )
    
    
    l10n_py_response_GlobalDocumentId = fields.Char(
        string='GlobalDocumentId',
        copy=False
        
    )

    
    l10n_py_response_CountryDocumentId = fields.Char(
        string='CountryDocumentId',
        copy=False
        
    )

    
    l10n_py_response_Messages = fields.Text(
        string='Messages',
        copy=False
    )
    
    
    l10n_py_response_ResponseValue = fields.Char(
        string='ResponseValue',
        copy=False
    )
    
    
    l10n_py_response_Code = fields.Integer(
        string='Code',
        copy=False
    )
    
    
    l10n_py_response_Description = fields.Char(
        string='Description',
        copy=False
    )
    
    
    l10n_py_response_ErrorException = fields.Text(
        string='ErrorException',
        copy=False
    )
    
    
    l10n_py_response_extra_info = fields.Text(
        string='l10n_py_response_extra_info',
    )
    

    
    l10n_py_response_request_document = fields.Text(
        string='Respuesta Consulta Cocumento',
    )
    
    
    
    edi_py_state = fields.Selection(
        string='Estado edi',
        selection=[
            ('sent', 'ENVIADO'), 
            ('observed', 'OBSERVADO'),
            ('pending', 'PENDIENTE'),
            ('canceled', 'CANCELADO')            
        ],
        default='pending',
        required=True,
        readonly=True,
        copy=False
    )

    
    establishment_id = fields.Many2one(
        string='Establecimiento',
        comodel_name='py.establishment',
    )

    
    expedition_point_id = fields.Many2one(
        string='Punto expedicion',
        comodel_name='expedition.point'
    )
    
    l10n_latam_document_number = fields.Char(
        string='Nro Documento', 
        readonly=True
    )

    
    invoice_number = fields.Char(
        string='Nro. Factura',
    )
    
    
    operation_condition = fields.Selection(
        string='Condicion de la operacion',
        selection= [ (key, value) for key , value in operacion_condition_dict.items() ],
        default='1',
        required=True
    )
    

    
    ringing_date_end = fields.Date(
        string='Fecha vencimiento de timbrado',
        copy=False
    )
    