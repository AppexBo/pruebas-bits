# -*- encoding: utf-8 -*-
{
    "name": "Facturacion (PY)",
    "version": "1.0",
    "description": """Modulo de operaciones (PY)""",
    "author": "Hinojosa Flores Luis Fernando",
    "website": "https://github.com/LuisFlores2170",
    'category': 'Accounting/Accounting',
    'depends': [
        'base', 
        'l10n_py_base',
        'account'
    ],
	"data":[
        'data/l10n_py_endpoint.xml',
        'views/account_move.xml',
        'report/paper_formats.xml',
        'report/layout.xml',
        'report/ir_actions_report.xml'
        
        
	],
    "installable": True,
    'license': 'LGPL-3',
    'maintainer': 'Luis Fernando Hinojosa Flores',
    'contributors': ['Luis Fernando Hinojosa Flores <clean.code.devs@gmail.com>']
}