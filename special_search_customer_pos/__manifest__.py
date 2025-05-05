{
	"name" : "Especial buscador de Clientes para el POS",
	"version" : "17.0.0.0",
	"category" : "Point of Sale",
	"depends" : [
		'base',
		'point_of_sale',
		'contacts',
	],
	"author": "AppexBo",
	'summary': 'Un buscador especializado para hacer una busqueda por campos especificos del cliente dentro de punto de venta',
	"description": "n buscador especializado para hacer una busqueda por campos especificos del cliente dentro de punto de venta",
	"website" : "https://www.appexbo.com/",
	"auto_install": False,
	"installable": True,
	"license": "LGPL-3",
	"data": [
        #'views/report_pdv_sale.xml'
	],
	'assets': {
		'point_of_sale._assets_pos': [
            "special_search_customer_pos/static/src/js/SearchCustomerWidget.js",
		],
	},
}