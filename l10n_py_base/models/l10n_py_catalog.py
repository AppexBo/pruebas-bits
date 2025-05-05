# -*- coding:utf-8 -*-

from odoo import api, models, fields

"""
    Archivo : Catalogos/Constantes de servicio PARAGUAY

"""


#--------------------------------------------------------------------------------------------------------------------------------
# Description: Tipo regimen
# File: data/l10n.py.regime.csv
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyRegime(models.Model):
    _name = 'l10n.py.regime'
    _description = 'Tipo de regimen'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"

    
    code = fields.Char(
        string='Codigo',
    )
    
    description = fields.Char(
        string='Descripcion',
    )
    
#--------------------------------------------------------------------------------------------------------------------------------    
# Paises
#--------------------------------------------------------------------------------------------------------------------------------
    
class L10nPyCountry(models.Model):
    _name = 'l10n.py.country'
    _description = 'Codigos paises'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code', 'representation')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description} - {record.representation}"

    
    code = fields.Char(
        string='Codigo',
    )
    
    description = fields.Char(
        string='Descripcion',
    )
    
    representation = fields.Char(
        string='Representacion',
    )
    
    information = fields.Text(
        string='Informacion',
    )

#--------------------------------------------------------------------------------------------------------------------------------
# Departamentos
#--------------------------------------------------------------------------------------------------------------------------------

class ResCity(models.Model):
    _inherit = ['res.city']
        
    code = fields.Char(
        string='Codigo',
    )

#--------------------------------------------------------------------------------------------------------------------------------
# Cuidades/Localidades
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyLocality(models.Model):
    _name = 'l10n.py.locality'
    _description = 'Localidades'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"

    description = fields.Char(string='Descripcion')
    code = fields.Integer(string='Codigo')

    
    res_city_id = fields.Many2one(
        string='Distrito',
        comodel_name='res.city',
    )

#--------------------------------------------------------------------------------------------------------------------------------
# Barrios
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyNeighborhood(models.Model):
    _name = 'l10n.py.neighborhood'
    _description = 'Barrios'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"

    description = fields.Char(string='Descripcion')
    code = fields.Integer(string='Codigo')

    
    l10n_py_locality_id = fields.Many2one(
        string='Localidad',
        comodel_name='l10n.py.locality',
    )
    
#--------------------------------------------------------------------------------------------------------------------------------
# Codigos unidades de medida
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyUom(models.Model):
    _name = 'l10n.py.uom'
    _description = 'Unidades de medida paraguay'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code', 'representation')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description} - {record.representation}"

    description = fields.Char(string='Descripcion')
    code = fields.Integer(string='Codigo')
    representation = fields.Char(string='Representacion')

#--------------------------------------------------------------------------------------------------------------------------------
# Codigos de afectacion (IMPUESTO)
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyTaxAffectationType(models.Model):
    _name = 'l10n.py.tax.affectation.type'
    _description = 'Codigos de afectacion (IMPUESTO)'

    
    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"

    description = fields.Char(string='Descripcion')
    code = fields.Integer(string='Codigo')
    


#--------------------------------------------------------------------------------------------------------------------------------
# Codigos de afectacion IVA
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyTaxAffectation(models.Model):
    _name = 'l10n.py.tax.affectation'
    _description = 'Codigos de afectacion IVA'

    
    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"

    description = fields.Char(string='Descripcion')
    code = fields.Integer(string='Codigo')
    

#--------------------------------------------------------------------------------------------------------------------------------
# Monedas
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyCurrency(models.Model):
    _name = 'l10n.py.currency'
    _description = 'Monedas paraguay'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('description', 'code')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"

    
    code = fields.Char(string='Código')
    
    number = fields.Char(
        string='Núm.',
    )
    
    dec = fields.Char(
        string='Dec.',
    )
    
    description = fields.Char(string='Descripcion')

#--------------------------------------------------------------------------------------------------------------------------------
# Codigos tipo de indentificacion
#--------------------------------------------------------------------------------------------------------------------------------

class L10nLatamIdentificationType(models.Model):
    
    _inherit = ['l10n_latam.identification.type']

    
    code = fields.Char(
        string='Codigo',
    )
    
#--------------------------------------------------------------------------------------------------------------------------------
# Tipo pago
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyPaymentType(models.Model):
    _name = 'l10n.py.payment.type'
    _description='Tipo de pago paraguay'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"
    
    description = fields.Char(
        string='Descripcion',
    )
    
    code = fields.Char(
        string='Codigo',
    )
    
#--------------------------------------------------------------------------------------------------------------------------------
# Tipo operacion
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyOperationType(models.Model):
    _name = 'l10n.py.operation.type'
    _description = 'Codigos tipo de operacion'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"
    
    description = fields.Char(
        string='Descripcion',
    )
    
    code = fields.Integer(
        string='Codigo',
    )
    
#--------------------------------------------------------------------------------------------------------------------------------
# Tipo transaccion
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyTransactionType(models.Model):
    _name = 'l10n.py.transaction.type'
    _description = 'Codigos tipo de transaccion'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"
    
    description = fields.Char(
        string='Descripcion',
    )
    
    code = fields.Integer(
        string='Codigo',
    )
    

#--------------------------------------------------------------------------------------------------------------------------------
# Tipo indicador de presencia
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyPresenceIndicator(models.Model):
    _name = 'l10n.py.presence.indicator'
    _description = 'Inicador depresencia'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"
    
    description = fields.Char(
        string='Descripcion',
    )
    
    code = fields.Integer(
        string='Codigo',
    )
    

#--------------------------------------------------------------------------------------------------------------------------------
# Tipo indicador de presencia
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyEconomicActivity(models.Model):
    _name = 'l10n.py.economic.activity'
    _description = 'Actividades economicas'

    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"
    
    description = fields.Char(
        string='Descripcion',
    )
    
    code = fields.Integer(
        string='Codigo',
    )
    
    
    type = fields.Selection(
        string='Tipo',
        selection=[('P', 'Principal'), ('S', 'Secundaria')]
    )
    
    def get_econonic_activity_id_info(self):
        return self.code, self.description
    


#--------------------------------------------------------------------------------------------------------------------------------
# Servicios HERMES
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyEndpoint(models.Model):
    _name = 'l10n.py.endpoint'
    _description = 'Servicios HERMES'

    name = fields.Char(
        string='Descripción'
    )

    
    operation_type = fields.Selection(
        string='Tipo operación',
        selection=[
            ('send', 'Envio'), 
            ('request', 'Solicitud')
        ]
    )
    

    url = fields.Char(
        string='URL',
        required=True
    )
    
    
    method = fields.Selection(
        [
            ('GET', 'GET'),
            ('POST', 'POST'),
            ('PUT', 'PUT'),
            ('DELETE', 'DELETE')
        ], 
        string="Método HTTP", 
        required=True
    )

    
    company_id = fields.Many2one(
        string='Compañia', 
        comodel_name='res.company', 
    )

    
    description = fields.Text(
        string='Descripción',
    )
    
#--------------------------------------------------------------------------------------------------------------------------------
# Codigos de denominacion de tarjeta 
# 1= Visa
# 2= Mastercard
# 3= American Express
# 4= Maestro
# 5= Panal
# 6= Cabal 99= Otro
#--------------------------------------------------------------------------------------------------------------------------------

class L10nPyCardDenomination(models.Model):
    _name = 'l10n.py.card.denomination'
    _description = 'Denominacíon de la tarjeta'
    name = fields.Char(
        string='Nombre',
        store=True,
        compute='_compute_name' 
    )
    
    @api.depends('code', 'description')
    def _compute_name(self):
        for record in self:
            record.name = f"({record.code}) {record.description}"
    
    description = fields.Char(
        string='Descripcion',
    )
    
    code = fields.Integer(
        string='Codigo',
    )
    

