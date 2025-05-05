# -*- coding:utf-8 -*-

from odoo import api, models, fields

class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']
    
    def get_E701(self):
        return self.product_id.getCode()
    
    def get_E708(self):
        return self.product_id.getDescription()
    
    def get_E709(self):
        return self.product_uom_id.getCode()
    
    def get_E710(self):
        return self.product_uom_id.getRepresentation()
    
    def get_E711(self):
        return self.quantity
    
    def get_E721(self):
        return round(self.price_unit,8)
    
    def get_E727(self):
        amount = self.get_E721() * self.get_E711()
        return round(amount, 8)
    
    def get_EA002(self):
        if self.discount>0:
            unit_price_disc = (self.price_total) / self.quantity
            discount = self.price_unit - unit_price_disc
            return round(discount,8)
        return 0
    
    def get_EA003(self):
        #return self.discount
        amount = (self.get_EA002()*100)/self.get_E721()
        return round(amount,8)
    
    
    
    def get_EA008(self):
        amount = 0
        if self.move_id.get_D013() in ['1','3','4','5']:
            amount = self.get_E721() - self.get_EA002()# - EA004 - EA006 - EA007
            amount *= self.get_E711()
        return round(amount, 8)
    
    def get_E731(self):
        return '1'
    
    def get_E732(self):
        return 'Gravado IVA'
    
    def get_E733(self):
        # Pendiente porcentaje gravado
        return 100
    
    def get_E734(self) -> float:
        amount = 0
        if self.get_E731() in ['2','3']:
            return 0
        # if self.get_E731() in ['1','4']:
        #     return 5
        if self.get_E731() in ['1','4']:
            return 10
        return amount
    
    def get_E735(self):
        amount = 0
        if self.get_E731() in ['2', '3']:
            return amount
        
        if self.get_E731() in ['1','4']:
            if self.get_E734() == 10:
                amount = ( self.get_EA008() * (self.get_E733() / 100)) / 1.1
            if self.get_E734() == 5:
                amount = ( self.get_EA008() * (self.get_E733() / 100)) / 1.05
                

            """
                [EA008* (E733/100)] / 1,1 si la tasa es del 10% 
                [EA008* (E733/100)] / 1,05 si la tasa es del 5%
            """
            
        return round(amount, 8)
    
    def get_E736(self):
        if self.get_E731() in ['2', '3']:
            return 0
        amount = self.get_E735() * (self.get_E734()/100)
        return round(amount, 8)
        

    
    def get_group_E_8_1(self):
        str_format = '<gValorItem>'

        E721 = self.get_E721()
        str_format += f'<dPUniProSer>{E721}</dPUniProSer>'
        
        E727 = self.get_E727()
        str_format += f'<dTotBruOpeItem>{E727}</dTotBruOpeItem>'
        
        str_format += self.get_group_E_8_1_1()
        
        str_format += '</gValorItem>'
        return str_format
    
    def get_group_E_8_1_1(self):
        str_format = '<gValorRestaItem>'
        EA002 = self.get_EA002()
        str_format += f'<dDescItem>{EA002}</dDescItem>'

        EA003 = ''
        if EA002>0:
            EA003 = self.get_EA003()
            str_format += f'<dPorcDesIt>{EA003}</dPorcDesIt>'
    

        
        EA008 = self.get_EA008()
        str_format += f'<dTotOpeItem>{EA008}</dTotOpeItem>'
        str_format += '</gValorRestaItem>'
        return str_format
    
    def get_group_E_8_2(self):
        str_format = '<gCamIVA>'
        E731 = self.get_E731()
        str_format += f'<iAfecIVA>{E731}</iAfecIVA>'

        E732 = self.get_E732()
        str_format += f'<dDesAfecIVA>{E732}</dDesAfecIVA>'
        
        E733 = self.get_E733()
        str_format += f'<dPropIVA>{E733}</dPropIVA>'
        
        E734 = self.get_E734()
        str_format += f'<dTasaIVA>{E734}</dTasaIVA>'
        
        E735 = self.get_E735()
        str_format += f'<dBasGravIVA>{E735}</dBasGravIVA>'
        
        E736 = self.get_E736()
        str_format += f'<dLiqIVAItem>{E736}</dLiqIVAItem>'
        
        str_format += '<dBasExe>0</dBasExe>'
        str_format += '</gCamIVA>'
        return str_format
    
    """
        (
            E721 (Precio unitario) – 
            EA002 (Descuento particular) – 
            EA004 (Descuento global) – 
            EA006 (Anticipo particular) – 
            EA007 (Anticipo global)
        ) * E711(cantidad)
    """