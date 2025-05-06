{
    'name': 'Report Movement History BitsAndCream',
    'version': '17.0.1.0.0',
    'category': 'Warehouse',
    'summary': "Muesta el historial del producto seleccionado.",
    'description': "Muesta el historial del producto seleccionado.",
    'author': 'AppexBo',
    'company': 'AppexBo',
    'maintainer': 'AppexBo',
    'website': 'https://www.appexbo.com/',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        
        'views/report_movement_history_views.xml',
        'views/report_historial_movimiento_xlsx',
        
        'report/moves_report_pdf.xml',
    ],
    'assets': {
        'web.assets_backend': [

        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
