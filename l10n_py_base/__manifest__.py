# -*- encoding: utf-8 -*-
{
    "name": "Paraguay modulo edi base",
    "version": "1.0",
    "description": """Modulo base para definicion de campos y estructura""",
    "author": "Hinojosa Flores Luis Fernando",
    "website": "https://github.com/LuisFlores2170",
    'category': 'Accounting/Accounting',
    'depends': [
        'base', 
        #'l10n_py_toponyms', 
        'l10n_py_vat',
        'uom',
        'account',
        'l10n_latam_invoice_document',
        'l10n_latam_base',
        'base_address_extended'
    ],
	"data":[
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        

        'data/l10n.py.uom.csv',
        'data/l10n_latam_document_type.xml',
        'data/l10n_latam.identification.type.csv',
        'data/l10n.py.payment.type.csv',
        'data/l10n.py.regime.csv',

        'data/l10n.py.country.csv',
        'data/res.country.state.csv',
        'data/res.city.csv',
        'data/l10n.py.locality.csv',
        'data/l10n.py.neighborhood.csv',
        'data/l10n.py.currency.csv',
        'data/l10n.py.tax.affectation.type.csv',
        'data/l10n.py.tax.affectation.csv',
        'data/l10n.py.operation.type.csv',
        'data/l10n.py.transaction.type.csv',
        'data/l10n.py.presence.indicator.csv',
        'data/l10n.py.card.denomination.csv',
        

        'views/uom_uom.xml',
        'views/account_move.xml',
        'views/res_country.xml',
        'views/res_currency.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
        'views/establishment_point.xml',
        
        'views/menu.xml',
        
	],
    "installable": True,
    'license': 'LGPL-3',
    'maintainer': 'Luis Fernando Hinojosa Flores',
    'contributors': ['Luis Fernando Hinojosa Flores <clean.code.devs@gmail.com>']
}