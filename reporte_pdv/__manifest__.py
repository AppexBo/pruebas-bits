# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "Reporte de ventas pdv",
	"version" : "17.0.0.0",
	"category" : "Point of Sale",
	"depends" : ['base','point_of_sale','account'],
	"author": "AppexBo",
	'summary': 'Reporte de ventas',
	"description": "REPORTES PDV",
	"website" : "https://www.appexbo.com/",
	
	"auto_install": False,
	"installable": True,
	#"images":['static/description/Banner.gif'],
	"license": "LGPL-3",
	"data": [
		#'security/ir.model.access.csv',  # Archivo de permisos
        'views/report_pdv_sale.xml'
	],
}