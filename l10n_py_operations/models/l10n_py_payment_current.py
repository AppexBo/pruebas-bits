# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError

class L10nPyPaymentCurrent(models.Model):
    _inherit = ['l10n.py.payment.currency']
    
    def get_E606(self):
        if self.l10n_py_payment_type_id:
            if self.l10n_py_payment_type_id.code not in ['1','3','4','5']:
                raise UserError(f'El metodo de pago: {self.l10n_py_payment_type_id.name}, no esta disponible')
            return self.l10n_py_payment_type_id.code
        raise UserError('Por favor establezca un metodo de pago')
    

    def get_E607(self):
        if self.l10n_py_payment_type_id:
            return self.l10n_py_payment_type_id.description
        raise UserError('Por favor establezca un metodo de pago')
    
    def get_E608(self):
        return self.amount
    
    
    def get_E609(self):
        return self.currency_id.getCode()
    
    def get_E610(self):
        return self.currency_id.getdDescription()
    
    
    def get_E611(self):
        return self.currency_id.get_py_rate()
    
    def get_E621(self):
        if self.card_denomination_id:
            return self.card_denomination_id.code
        else:
            raise UserError('Establezca una denominacion de la tarjeta')
    def get_E622(self):
        if self.card_denomination_id:
            return self.card_denomination_id.description
        else:
            raise UserError('Establezca una denominacion de la tarjeta')
    
    def get_E626(self):
        return 1 # 1 = POS
    
    def get_E629(self):
        return self.card

    def get_group_7_1_1(self):
        str_format = '<gPagTarCD>'

        E621 = self.get_E621()
        str_format += f'<iDenTarj>{E621}</iDenTarj>'
        
        
        E622 = self.get_E622()
        str_format += f'<dDesDenTarj>{E622}</dDesDenTarj>'
        
        E626 = self.get_E626()
        str_format += f'<iForProPa>{E626}</iForProPa>'
        
        E629 = self.get_E629()
        str_format += f'<dNumTarj>{E629}</dNumTarj>'
        

        str_format += '</gPagTarCD>'

        return str_format