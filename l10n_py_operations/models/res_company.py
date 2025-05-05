# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import html

class ResCompany(models.Model):
    
    _inherit = ['res.company']
    
    def getRUC(self):
        if self.vat:
            return self.vat.split('-')[0]
        raise UserError(f'No tiene establesido un codigo RUC para la empresa: {self.name}')
    
    def getDigitVerRUC(self):
        if self.vat:
            return self.vat[-1]
        return ''
    
    def get_taxpayer_type(self):
        if self.taxpayer_type:
            return self.taxpayer_type
        raise UserError(f'La compañia: {self.name}, no tiene establecido en tipo de contribuyente')
    
    def get_name_reazon_social(self):
        if self.use_endpoints_test:
            return 'DE generado en ambiente de prueba - sin valor comercial ni fiscal'
        return html.escape(self.name)
    
    def get_number_house(self):
        return self.number_house if self.number_house else '0'
    
    def get_address(self):
        if self.street:
            return html.escape(self.street)
        raise UserError(f'La compañia: {self.name}, no tiene la direccion establecida en el RUC')
    
    def get_department_info(self):
        if self.state_id:
            return self.state_id.get_department_info()
        raise UserError(f'La compañia: {self.name}, no tiene un departamento establecido')
        
    def get_department_distrit_info(self):
        if self.distrit_id:
            return self.distrit_id.get_department_distrit_info()
        raise UserError(f'La compañia: {self.name}, no tiene un distrito establecido')
        
    def get_department_distrit_city_info(self):
        if self.locality_id:
            return self.locality_id.get_department_distrit_city_info()
        raise UserError(f'La compañia: {self.name}, no tiene una cuidad/localidad establecida')

    def get_document_issuer_phone_number(self):
        if self.document_issuer_phone_number:
            return self.document_issuer_phone_number
        raise UserError(f'La compañia: {self.name}, no tiene un numero de telefono emisor establecido')

    def get_emisor_email(self):
        if self.email:
            return self.email
        raise UserError(f'La compañia: {self.name}, no tiene un correo establecido')
    
    def get_econonic_activity_id_info(self):
        if self.econonic_activity_id:
            return self.econonic_activity_id.get_econonic_activity_id_info()
        raise UserError(f'La compañia: {self.name}, no tiene una actividad economica principal establecida')
    

    def get_sync_point_id(self):
        if self.sync_point:
            return self.sync_point
        raise UserError(f'La compañia: {self.name}, no tiene un SyncPointId')


    def get_api_key(self):
        if self.api_key:
            return self.api_key
        raise UserError(f'La compañia: {self.name}, no se encontro un API KEY')


    def get_py_mapping(self):
        if self.py_mapping:
            return self.py_mapping
        raise UserError(f'La compañia: {self.name}, no se encontro un mapping establecido')
    
    def get_ringing_date(self):
        ringing = self.ringing_ids.filtered(lambda ring: ring.use)
        if ringing:
            return ringing[0].date_init.strftime("%Y-%m-%d")
        raise UserError(f'La compañia: {self.name}, no se encontro un timbrado establecido')
    
    def get_ringing_date_end(self, to_xml = False):
        ringing = self.ringing_ids.filtered(lambda ring: ring.use)
        if ringing:
            return ringing[0].date_end.strftime("%Y-%m-%d") if to_xml else ringing[0].date_end
        #raise UserError(f'La compañia: {self.name}, no se encontro un timbrado establecido')
    
    
    def get_ringing_code(self):
        ringing = self.ringing_ids.filtered(lambda ring: ring.use)
        if ringing:
            return ringing[0].name
        raise UserError(f'La compañia: {self.name}, no se encontro un timbrado establecido')
    