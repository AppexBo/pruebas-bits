# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import html

class ResPartner(models.Model):
    _inherit = ['res.partner']
    
    def get_receiver_nature(self):
        if self.receiver_nature:
            return self.receiver_nature
        raise UserError(f'Cliente: {self.name}, no se establecio la naturaleza del receptor')
    
    def get_receiver_operation(self):
        if self.operation_type_id:
            return self.operation_type_id.code
        raise UserError(f'Cliente: {self.name}, no se establecio un tipo de operacion')

    def get_country_info(self):
        if self.country_id:
            return self.country_id.get_country_info()
        raise UserError(f'Cliente: {self.name}, no se establecio un pais')

    def get_taxpayer_type(self):
        if self.receiver_nature == '1':
            if self.taxpayer_type:
                return self.taxpayer_type
            raise UserError(f'Cliente: {self.name}, no se establecio un tipo de contribuyente')
        return ''
    
    def get_ruc(self):
        if self.receiver_nature == '1':
            if self.vat:
                return self.vat.split('-')[0]
            raise UserError(f'Cliente: {self.name}, no se establecio RUC')
        return ''
    
    def get_digit_ver(self):
        if self.get_ruc():
            dv = self.vat.split('-')
            if len(dv)>1:
                return dv[1]
            raise UserError(f'No se encontro el digito verificador para el cliente: {self.name}')
        return ''
    
    def get_reciver_name(self):
        return html.escape(self.name)
    
    def get_D208(self):
        if self.l10n_latam_identification_type_id:
            code = self.l10n_latam_identification_type_id.code
            if code:
                if code =='5' and self.get_receiver_nature() == '2':
                    raise UserError(f"Cliente: {self.name}, Tipo de indentificacion Innominado, por favor enviar naturaleza del receptor como: Contribuyente, y Nro Identificacion: 0-0")
                return code
            raise UserError(f"Cliente: {self.name}, Tipo de identificacion: FALSE, para tipo de naturaleza: {self.receiver_nature}, Cuando la naturaleza del receptor sea (No contribuyente), se recomienda usar un Tipo de identificacion a (RUC)")
        raise UserError(f'Cliente: {self.name}, no se establecio Tipo de identificación')

    def get_D209(self):
        if self.l10n_latam_identification_type_id:
            return self.l10n_latam_identification_type_id.name
        raise UserError(f'Cliente: {self.name}, no se establecio Tipo de identificación')

    def get_vat(self):
        if self.l10n_latam_identification_type_id:
            return self.vat
        raise UserError(f'Cliente: {self.name}, no se establecio Tipo de identificación')

    
    def get_D213(self):
        if self.street:
            return html.escape(self.street)
        raise UserError(f'Cliente: {self.name}, no se establecio una direccion')
    
    def get_D218(self):
        if self.house_number:
            return self.house_number
        raise UserError(f'Cliente: {self.name}, no se un numero de casa')        
    
    def get_department_info(self):
        if self.state_id:
            return self.state_id.get_department_info()
        return '',''
    
    def get_department_distrit_info(self):
        if self.distrit_id:
            return self.distrit_id.get_department_distrit_info()
        return '', ''
    
    def get_department_distrit_city_info(self):
        if self.locality_id:
            return self.locality_id.get_department_distrit_city_info()
        return '', ''