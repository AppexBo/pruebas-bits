# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = ['account.move']

    # PLUS FIELDS

    
    company_vat = fields.Char(
        string='RUC EMPRESA',
        related='company_id.vat',
        readonly=True,
        store=True
    )

    
    establishment_code = fields.Char(
        string='Código de establecimiento',
        related='establishment_id.code',
        readonly=True,
        store=True
    )

    expedicion_point_code = fields.Char(
        string='Código punto de expedicion',
        related='expedition_point_id.code',
        readonly=True,
        store=True
    )

    
    

    #-------------------------------------------------------------------------------------
    
    

    
    identity_document_type_id = fields.Many2one(
        string='Tipo identificación',
        comodel_name='l10n_latam.identification.type',
        related='partner_id.l10n_latam_identification_type_id',
        readonly=True,
        store=True,
        help='Seleccionar si se trata de RUC, CÉDULA DE IDENTIDAD, PASAPORTE, CARNÉ DE MIGRACIÓN'
    )
    
    
    identification_number = fields.Char(
        string='RUC/ Identificación',
        related='partner_id.vat',
        readonly=True,
        store=True,
        help='Consignar el N° del tipo de identificación indicado. Tratándose de un comprador no identificado se indicará como RUC el número 44444401, en cuyo caso en la columna 3 se consignará "Consumidor Final". Tratándose de operaciones con clientes extranjeros sin domicilio o residencia en el país, se indicará como RUC el número 88888801. En caso de que el tipo de comprobante sea liquidación de salario, en la presente columna se deberá colocar el RUC del empleador/pagador.'
    )

    # NOMBRE RAZON SOCIAL
    
    
    international_organization_agency = fields.Char(
        string='Organismo o Agencia Internacional',
        copy=False,
        help='Seleccionar el nombre del organismo o agencia internacional acreditada en el país, conforme a la Ley. Ejemplo: KOICA, JICA, OEA, OMS, GIZ, FMI, ETC.'
    )

    
    
    ringing_code = fields.Char(
        string='Timbrado',
        help='Consignar el N° de timbrado. Aplicable únicamente para aquellos comprobantes de venta que deben ser timbrados conforme al Decreto y sus modificaciones',
        copy=False
    )



    
    def get_C004(self):
        ringing_code = super(AccountMove, self).get_C004()
        self.write({'ringing_code' : ringing_code, 'ringing_date_end' : self.company_id.get_ringing_date_end()})
        return ringing_code
    

    
    amount_total_invoice = fields.Float(
        string='Monto total facturado',
        copy=False
    )

    def get_F014(self):
        dTotGralOpe = super(AccountMove, self).get_F014()
        self.write({'amount_total_invoice' : dTotGralOpe})
        return dTotGralOpe
    
    
    total_base_taxed_10_percent = fields.Float(
        string='Base total gravada al 10%',
        copy=False
    )
    
    total_base_iva_10_percent = fields.Float(
        string='Base imponible total IVA al 10%',
        copy=False
    )
    
    def get_total_base_taxed_10_percent(self):
        amount_grav = 0
        amount_iva = 0

        for line in self.invoice_line_ids:
                if line.display_type == 'product':
                    if line.taxes_percentage_type == '10':
                        amount_grav += line.get_E735()
                        amount_iva = line.get_E736()
        
        self.write({'total_base_taxed_10_percent' : amount_grav})
        self.write({'total_base_iva_10_percent' : amount_iva})
        

    total_base_taxed_5_percent = fields.Float(
        string='Base total gravada al 5%',
        copy=False
    )

    total_base_iva_5_percent = fields.Float(
        string='Base imponible total IVA al 5%',
        copy=False
    )


    def get_total_base_taxed_5_percent(self):
        amount_grav = 0
        amount_iva = 0

        for line in self.invoice_line_ids:
                if line.display_type == 'product':
                    if line.taxes_percentage_type == '5':
                        amount_grav += line.get_E735()
                        amount_iva = line.get_E736()
        
        self.write({'total_base_taxed_5_percent' : amount_grav})
        self.write({'total_base_iva_5_percent' : amount_iva})

    l10n_py_purchase_document_type_dic = {
        'electronic' : 'ELECTRONICO',
        'printed' : 'IMPRESO'
    }

    
    purchase_document_type = fields.Selection(
        string='Tipo documento compra',
        selection= [ (key, value) for key , value in l10n_py_purchase_document_type_dic.items() ],
        default='electronic'
    )
    

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for record in self:
            if record.move_type=='in_invoice':
                record.get_F014()
                record.get_total_base_taxed_10_percent()
                record.get_total_base_taxed_5_percent()
        return res