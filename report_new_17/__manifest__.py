# -*- coding:utf-8 -*-
{
    'name': 'Reporte Contable vs17',
    'version': '1.0',
    'depends': [
        'base', 
        'l10n_bo',
        'account',
        'purchase',
    ],
    'author': 'APPEX BOLIVIA SRL.',
    'summary': 'Reporte pdf de los asientos contables con un formato personalizado',
    'data': [
        'reports/paper_format.xml',  # Verifica que este archivo existe y tiene el contenido correcto
        'reports/layout_standart_account_account.xml',  # Verifica que este archivo existe y tiene el contenido correcto
        'reports/account_account.xml',  # Verifica que este archivo existe y tiene el contenido correcto
    ],
    'installable': True,
}