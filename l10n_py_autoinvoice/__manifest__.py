# -*- encoding: utf-8 -*-
{
    "name": "Autofactura electrónica (PY)",
    "version": "1.0",
    "description": """Comprobante de venta electrónico (PY)""",
    "author": "Hinojosa Flores Luis Fernando",
    "website": "https://github.com/LuisFlores2170",
    'category': 'Accounting/Accounting',
    'depends': [
        'base', 
        'account',
        'l10n_py_base',
        'l10n_py_operations'
    ],
	"data":[
        'data/l10n_latam_document_type.xml'
	],
    "installable": True,
    'license': 'LGPL-3',
    'maintainer': 'Luis Fernando Hinojosa Flores',
    'contributors': ['Luis Fernando Hinojosa Flores <clean.code.devs@gmail.com>']
}