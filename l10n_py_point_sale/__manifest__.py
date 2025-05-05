# -*- encoding: utf-8 -*-
{
    "name": "Punto de venta (PY)",
    "version": "1.0",
    "description": """Facturacion paraguay POS""",
    "author": "Hinojosa Flores Luis Fernando",
    "website": "https://github.com/LuisFlores2170",
    'category': 'Accounting/Accounting',
    'depends': [
        'base', 
        'l10n_py_base',
        'l10n_py_operations',
        'account',
        'point_of_sale'
    ],
	"data":[
        'views/pos_payment_method.xml',
        'views/pos_config.xml',
        'views/pos_order.xml',
        
	],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_py_point_sale/static/src/**/*',
        ],
        
    },
    "installable": True,
    'license': 'LGPL-3',
    'maintainer': 'Luis Fernando Hinojosa Flores',
    'contributors': ['Luis Fernando Hinojosa Flores <clean.code.devs@gmail.com>']
}