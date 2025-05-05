# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime, time
import hashlib
import pytz


from odoo.exceptions import ValidationError, UserError

class PyGroups(models.Model):
    _inherit = ['account.move']
    
    def get_AA002(self):
        return 150
    
    def get_A003(self):
        return ''
    
    def get_A004(self):
        return ''
    
    
    def get_A005(self):
        return 1
    
    def get_B002(self):
        if self.expedition_point_id:
            return self.expedition_point_id.get_emision_code()
        raise UserError("No se encotro un punto de expedicion")
    
    def get_B003(self):
        return self.expedition_point_id.get_emision_description()
    
    def get_B004(self, nit, numero_factura, punto_venta="001"):
        ahora = datetime.now()
        base = f"{nit}{numero_factura}{punto_venta}{ahora.year}{ahora.month:02d}{ahora.day:02d}{ahora.hour:02d}{ahora.minute:02d}"
        hash_obj = hashlib.sha256(base.encode())
        codigo_seguro = int(hash_obj.hexdigest()[:9], 16) % 10**9
        return f"{codigo_seguro:09d}"
    
    def get_B005(self):
        return ''
    
    def get_B006(self):
        dInfoFisc = ''
        for line in self.get_invoice_items():
            dInfoFisc += line.product_id.get_product_tag_ids_description(self.get_C002() == '7')
        return dInfoFisc
    
    
    def get_C002(self)->str:
        "Codigo Tipo de Documento Electrónico"
        return self.l10n_latam_document_type_id.code
        
    
    def get_C003(self)->str:
        "Descripción del tipo de documento electrónico"
        return self.l10n_latam_document_type_id.name
    
    def get_C004(self):
        return self.company_id.get_ringing_code() #'80102544'
    
    def getRUC(self):
        return self.company_id.getRUC()
    
    def getDigitVerRUC(self):
        return self.company_id.getDigitVerRUC()
    
    def get_serial_number(self):
        if self.l10n_latam_document_type_id and self.expedition_point_id:
            sequence_ids : models.Model = self.expedition_point_id.expedition_point_sequence_ids
            sequence_id = sequence_ids.filtered(lambda s:s.name.id == self.l10n_latam_document_type_id.id)
            if sequence_id:
                number = sequence_id[0].get_serial()
                return number
        return ''
    
    def next_sequence(self):
        if self.l10n_latam_document_type_id and self.expedition_point_id:
            sequence_ids : models.Model = self.expedition_point_id.expedition_point_sequence_ids
            sequence_id = sequence_ids.filtered(lambda s:s.name.id == self.l10n_latam_document_type_id.id)
            if sequence_id:
                return sequence_id[0].next_sequence()
        
    
    def get_invoice_number(self, ir_next = False):
        if self.l10n_latam_document_type_id and self.expedition_point_id:
            sequence_ids : models.Model = self.expedition_point_id.expedition_point_sequence_ids
            sequence_id = sequence_ids.filtered(lambda s:s.name.id == self.l10n_latam_document_type_id.id)
            if sequence_id:
                number = sequence_id[0].get_sequence()
                if ir_next:
                    self.write({'invoice_number' : str(number)})
                    sequence_id[0].next_sequence()
                return number

        raise UserError('No tiene una secuencia de documento generado')
    
    def get_C008(self) -> str:
        "Fecha inicio de vigencia del timbrado"
        return self.get_ringing_date(to_xml=True)
    
    def get_ringing_date(self, to_xml = False):
        return self.company_id.get_ringing_date()
    
    def get_C009(self)->str:
        "Fecha fin de vigencia del timbrado"
        return self.get_ringing_date_end(to_xml=True)

    def get_ringing_date_end(self, to_xml = False):
        return self.company_id.get_ringing_date_end(to_xml)
    
    def get_emision_date(self):
        tz_paraguay = pytz.timezone('America/Asuncion')
        now_paraguay = datetime.now(tz_paraguay)

        if self.invoice_date:
            invoice_date_dt = datetime.combine(self.invoice_date, time(0, 0))
            invoice_date_paraguay = tz_paraguay.localize(invoice_date_dt, is_dst=None)  
        else:
            invoice_date_paraguay = now_paraguay

        emision_datetime = datetime.combine(invoice_date_paraguay.date(), now_paraguay.time())

        self.write({'l10n_py_emision_date': emision_datetime.replace(tzinfo=None)})

        # Retornar en formato ISO 8601
        return emision_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    
    

    
    def get_taxpayer_type(self):
        return self.company_id.get_taxpayer_type()
    
    def get_name_reazon_social(self):
        return self.company_id.get_name_reazon_social()

    def get_address(self):
        return self.company_id.get_address()
    
    def get_number_house(self):
        return self.company_id.get_number_house()

    def get_department_info(self):
        return self.company_id.get_department_info()
    
    def get_department_distrit_info(self):
        return self.company_id.get_department_distrit_info()
    
    def get_department_distrit_city_info(self):
        return self.company_id.get_department_distrit_city_info()
    
    def get_document_issuer_phone_number(self):
        return self.company_id.get_document_issuer_phone_number()
    
    def get_emisor_email(self):
        return self.company_id.get_emisor_email()
    
    def get_econonic_activity_id_info(self):
        return self.company_id.get_econonic_activity_id_info()
    
    # RECEPTOR

    def get_receiver_nature(self):
        return self.partner_id.get_receiver_nature()
    
    def get_receiver_operation(self):
        return self.partner_id.get_receiver_operation()
    
    def get_receiver_country_info(self):
        return self.partner_id.get_country_info()
    
    def get_receiver_taxpayer_type(self):
        return self.partner_id.get_taxpayer_type()
    
    def get_receiver_ruc(self):
        return self.partner_id.get_ruc()
    
    def get_receiver_digit_ver(self):
        return self.partner_id.get_digit_ver()
    
    def get_receiver_name(self):
        return self.partner_id.get_reciver_name()
    

    def get_D011(self):
        "Codigo Tipo de transacción"
        if self.l10n_py_transaction_type_id:
            return self.l10n_py_transaction_type_id.code
        raise UserError("No se encontro un tipo de operacion en la factura")
    
    def get_D012(self):
        "Tipo de transacción"
        return self.l10n_py_transaction_type_id.description
    

    def get_D013(self):
        "Codigo Tipo de afectado"
        if self.l10n_py_tax_affectation_type:
            return str(self.l10n_py_tax_affectation_type.code)
        raise UserError("No se encontro un tipo de impuesto afectado en la factura")
    
    def get_D014(self):
        "Descripción del tipo de impuesto afectado"
        return self.l10n_py_tax_affectation_type.description
    
    def get_D015(self):
        return self.currency_id.getCode()
    
    def get_D016(self):
        return self.currency_id.getdDescription()
    
    def get_D017(self):
        # pendiente
        return '1'
    
    def get_D018(self):
        return 1
    
    def get_D208(self):
        return self.partner_id.get_D208()
    
    def get_D209(self):
        return self.partner_id.get_D209()
    
    def get_D210(self):
        return self.partner_id.get_vat()
    
    def get_D213(self):
        return self.partner_id.get_D213()
    
    def get_D218(self):
        return self.partner_id.get_D218()
    
    
    def get_receiver_department_info(self):
        return self.partner_id.get_department_info()
    
    def get_receiver_department_distrit_info(self):
        return self.partner_id.get_department_distrit_info()
    
    def get_receiver_department_distrit_city_info(self):
        return self.partner_id.get_department_distrit_city_info()
    
    
    def get_E011(self):
        if self.l10n_py_presence_indicator_id:
            if self.l10n_py_presence_indicator_id.code != 1:
                raise UserError(f'Tipo de operacion: {self.l10n_py_presence_indicator_id.name}, no disponible')
            return self.l10n_py_presence_indicator_id.code
        raise UserError('Por favor establezca un indicador de presencia')

    def get_E012(self):
        if self.l10n_py_presence_indicator_id:
            return self.l10n_py_presence_indicator_id.description
        raise UserError('Por favor establezca un indicador de presencia')
    
    def get_E601(self):
        if self.operation_condition:
            return self.operation_condition
        raise UserError('No se encontro una condicion de operacion: Credito/Contado')
    
    def get_E602(self):
        if self.operation_condition:
            return self.operacion_condition_dict.get(self.operation_condition, '')
        raise UserError('No se encontro una condicion de operacion: Credito/Contado')
    
     
    #cedula, crokis, agua, luz, 
    
    
    #def get_F004(self):


    def get_F005(self):
        #if self.get_E731
        amount = 0
        for line in self.invoice_line_ids:
            if line.display_type == 'product':  
                amount += line.get_EA008()
        return amount
    

    
    def get_F008(self):
        if self.get_D013() in ['1','3','4','5']:
            return self.get_F005() # + F002 + F003 +  F004 # PENDIENTE
        return 0
    
    def get_F009(self):
        amount = 0
        for line in self.invoice_line_ids:
            if line.display_type == 'product':
                amount += line.get_EA002()
        return amount
    
    def get_F026(self):
        #pendiente
        return 0
    
    def get_F033(self):
        amount = 0
        # for line in self.invoice_line_ids:
        #     if line.display_type == 'product':
        #         amount += line.get_EA004()
        return amount
    
    def get_F034(self):
        # pendiente suma de anticipos
        return 0
    
    def get_F035(self):
        # pendiente suma de anticipos
        return 0
    
    def get_F036(self):
        # pendiente liquidacion del iva por redondeo 5 %
        return 0
    
    def get_F037(self):
        # pendiente liquidacion del iva por redondeo 10 %
        return 0
    
    
    def get_F010(self):
        amount = 0
        
        return amount
    
    def get_F011(self):
        amount = self.get_F009()# + self. ...
        return amount
    
    def get_F012(self):
        # pendiente anticipos
        return 0
    
    def get_F013(self):
        # consulta calculo de redondeo
        return 0
    
    def get_F014(self):
        #raise UserError(f"OP: {self.get_F008()} - {self.get_F013()}")
        amount = self.get_F008() - self.get_F013() # + self.get_F025()
        return amount
    
    def get_F015(self):
        # pendiente IVA 5 %
        return 0
    
    def get_F016(self):
        amount = 0
        for line in self.invoice_line_ids:
            if line.display_type == 'product' and line.get_E734() == 10:
                amount += line.get_E736()
        return  round(amount, 8)
    
    def get_F017(self):
        amount = self.get_F015() + self.get_F016() - self.get_F036() - self.get_F037() + self.get_F026()
        return round(amount, 8)
    
    def get_F018(self):
        # pendiente
        return 0
    
    def get_F019(self):
        amount = 0
        for line in self.invoice_line_ids:
            if line.display_type == 'product' and line.get_E734() == 10:
                amount += line.get_E735()
        return round(amount, 8)
    
    def get_F020(self):
        amount = self.get_F018() + self.get_F019()
        return round(amount, 8)
    
    def get_F023(self):
        if self.get_D017() == '1':
            return self.get_F014() * self.get_D018()
        
        #... pendiente terminar
        
        return 0
        
    
    def get_FecFirma(self):
        self.write({'l10n_py_invoice_sign_date' : fields.datetime.now()})
        fecha_hora_paraguay = self.l10n_py_invoice_sign_date.astimezone(pytz.timezone('America/Asuncion'))
        return fecha_hora_paraguay.strftime("%Y-%m-%dT%H:%M:%S")

    def get_C005(self):
        if self.establishment_id:
            return self.establishment_id.get_code()
        raise UserError("Por favor establezca un punto de establecimiento")
    
    def get_C006(self):
        if self.expedition_point_id:
            if self.expedition_point_id.establishment_id.id == self.establishment_id.id:
                return self.expedition_point_id.get_code() #'002'
            raise UserError("El punto de expedicion no corresponde al esteblecimiento.")            
        raise UserError("Por favor establezca un punto de expedición")
