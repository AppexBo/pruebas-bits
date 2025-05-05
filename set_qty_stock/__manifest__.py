{
	"name" : "Modulo de automatizacion de asignacion de cantidades",
	"version" : "17.0.0.0",
	"category" : "Point of Sale",
	"depends" : [
		'base',
		'stock',
	],
	"author": "AppexBo",
	'summary': 'Boton en Warehouse pedidos en proceso',
	"description": "Boton para asignar las cantidades aunque no hayan",
	"website" : "https://www.appexbo.com/",
	
	"auto_install": False,
	"installable": True,
	
	"license": "LGPL-3",
	"data": [
		'views/stock_picking_views.xml'
	],
}