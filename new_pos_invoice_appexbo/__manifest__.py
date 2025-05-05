# -*- coding: utf-8 -*-
{
    'name': "POS cambio de formato factura",

    'summary': """
        Modulo creado para estilo de factura especial
    """,

    'description': """
        Modulo creado para estilo de factura especial
    """,

    'author': "AppexBO",
    'website': "https://www.appexbo.com/",

    'category': 'Point of Sale',
    'version': '17.0.0.1',

    'depends': [
        'l10n_sa_pos'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'new_pos_invoice_appexbo/static/src/xml/OrderReceipt.xml',
        ],
    },
    
    'installable': True,
    'auto_install': False,
    "license": "LGPL-3",
}
