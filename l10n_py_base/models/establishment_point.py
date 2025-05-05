# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError


class ExpeditionPointSequence(models.Model):
    _name = 'expedition.point.sequence'
    _description = 'Secuencia de puntos de expedición'

    
    name = fields.Many2one(
        string='Documento',
        comodel_name='l10n_latam.document.type',
        required=True
    )

    
    serial = fields.Char(
        string='Serie',
        help='AA,AB,AC,...',
    )
    
    
    
    sequence = fields.Integer(
        string='Secuencia',
        default=1,
        help='MAX=9999999',
    )
    
    
    expedition_point_id = fields.Many2one(
        string='Punto de expedicion',
        comodel_name='expedition.point',
    )

    def get_serial(self):
        return self.serial or ''
    
    def get_sequence(self):
        if self.sequence > 9999999:
            raise UserError('El numero de emisiones documento/factura a llegado al limite, el limite es 9999999')
        return str(self.sequence).zfill(7)
    
    def next_sequence(self):
        if self.sequence <= 9999999:
            self.write(
                {
                    'sequence' : self.sequence + 1
                }
            )    

    
    
    

class ExpeditionPoint(models.Model):
    _name = 'expedition.point'
    _description = 'Punto de expedición'

    emision_type_dict = {
        '1' : 'Normal',
        '2' : 'Contingencia'
    }
    
    
    name = fields.Char(
        string='Nombre',
        required=True,
        copy=False
    )
    
    code = fields.Char(
        string='Codigo',
        required=True,
        copy=False
    )
    
    establishment_id = fields.Many2one(
        string='Establecimiento',
        comodel_name='py.establishment',
        required=True
    )

    
    emision_type = fields.Selection(
        string='Tipo emision',
        selection= [ (key, value) for key , value in emision_type_dict.items() ],
        default='1',
        required=True
    )
    

    
    expedition_point_sequence_ids = fields.One2many(
        string='Secuencias de punto de expedición',
        comodel_name='expedition.point.sequence',
        inverse_name='expedition_point_id',
    )
    
    
    company_id = fields.Many2one(
        string='Compañia', 
        comodel_name='res.company',
        default=lambda self: self.env.company
    )
    
    def get_code(self):
        if not self.code:
            raise UserError(f'No se encontro codigo para el {self._description}: {self.name}')
        return str(self.code).zfill(3) if len(self.code) !=3 else self.code
    
    def get_emision_code(self):
        return self.emision_type
    
    def get_emision_description(self):
        return self.emision_type_dict.get(self.emision_type, '')
    
    
    
    

class Establishment(models.Model):
    _name = 'py.establishment'
    _description = 'Establecimiento'

    
    company_id = fields.Many2one(
        string='Compañia', 
        comodel_name='res.company',
        default=lambda self: self.env.company
    )
    

    
    name = fields.Char(
        string='Nombre',
        copy=False,
        required=True
    )
    
    
    code = fields.Char(
        string='Codigo',
        copy=False,
        required=True
    )
    
    def get_code(self):
        if not self.code:
            raise UserError(f'No se encontro codigo para el {self._description}: {self.name}')
        return str(self.code).zfill(3) if len(self.code) !=3 else self.code
    
    
    expedition_point_ids = fields.One2many(
        string='Punto de expedición',
        comodel_name='expedition.point',
        inverse_name='establishment_id',
    )
    