# -*- coding:utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError

class ResPartner(models.Model):
    
    _inherit = ['res.partner']
    
    
    def write(self, values : dict):
        #raise UserError(f"{values}")
        if values.get('receiver_nature', False):
            values['receiver_nature'] = str(values['receiver_nature'])

        result = super(ResPartner, self).write(values)
    
        return result
    