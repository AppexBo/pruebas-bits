# -*- encoding: utf-8 -*-

{
    'name': 'Verifcador Base VAT PY',
    "version": "1.0",
    "description": """Verificador RUC""",
    "author": "Hinojosa Flores Luis Fernando",
    "website": "https://github.com/LuisFlores2170",
    'category': 'Sales/CRM',
    'depends': ['base', 'contacts', 'base_vat', 'l10n_latam_base'],
    'data' : [
        'views/res_partner.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
    'maintainer': 'Luis Fernando Hinojosa Flores',
    'contributors': ['Luis Fernando Hinojosa Flores <hinojosafloresluisfernando@gmail.com>']
}