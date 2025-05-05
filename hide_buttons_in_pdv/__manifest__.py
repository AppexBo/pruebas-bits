{
    'name': 'Ocultar campos',
    'version': '17.0.0.2',
    'description': '',
    'summary': 'Ocultar campos del PDV (punto de venta)',
    
    'author': 'Erick Denis Mercado Oudalova',
    'maintainer': 'AppexBo',
    'company': 'AppexBo',
    'website': 'https://www.appexbo.com/',
    
    'category': 'Point of Sale',
    'depends': [
        'point_of_sale',
    ],
    'data': [
    #    'views/pos_template.xml',   
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'hide_buttons_in_pdv/static/**/*',
        ],
    },
    'license': 'AGPL-3',
}
