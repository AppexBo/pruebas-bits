# -*- encoding: utf-8 -*-

{
    'name': 'Libro de compras y ventas',
    "version": "1.0",
    "description": """Modelo de libro de ventas, ingresos, compras, egresos""",
    "author": "Hinojosa Flores Luis Fernando",
    "website": "https://github.com/LuisFlores2170",
    'category': 'Sales/CRM',
    'depends': ['l10n_py_base', 'l10n_py_operations', 'account', 'l10n_latam_base'],
    'data' : [
        'views/account_move.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
    'maintainer': 'Luis Fernando Hinojosa Flores',
    'contributors': ['Luis Fernando Hinojosa Flores <hinojosafloresluisfernando@gmail.com>']
}