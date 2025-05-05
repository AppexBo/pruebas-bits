# -*- encoding: utf-8 -*-


import string

import logging
_logger = logging.getLogger(__name__)



from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    ruc_state = fields.Selection(
        string='Estado RUC',
        selection=[
            ('to_check', 'Verificar'), 
            ('valid', 'VALIDO'), 
            ('invalid', 'INVALIDO')
        ],
        default='to_check',
        readonly=True 
    )

    
    is_ruc = fields.Boolean(
        string='¿Es RUC?',
        related='l10n_latam_identification_type_id.is_vat',
        readonly=True,
        store=True
    )
    
    
    
    @api.onchange('vat')
    @api.constrains('vat')
    def _check_vat_py(self):
        for record in self:
            ruc_state = 'to_check'
            if record.vat and record.is_ruc:
                ruc_state = 'valid' if record.check_vat_py(record.vat) else 'invalid'
            record.write({'ruc_state' : ruc_state})
    
    

    def check_vat_py(self, vat):
        ruc = ''
        basemax = 11
        for c in str(vat).replace('-', ''):
            ruc += c.isdigit() and c or str(ord(c))
        k = 2
        total = 0
        for c in reversed(ruc[:-1]):
            n = int(c)
            if n > basemax:
                k = 2
            total += n * k
            k += 1
        resto = total % basemax
        if resto > 1:
            n = basemax - resto
        else:
            n = 0
        res = n == int(ruc[-1])
        _logger.info(f"ESTADO DEL RUC: {res}")
        return res