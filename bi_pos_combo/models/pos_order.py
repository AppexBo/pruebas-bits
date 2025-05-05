# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID
from functools import partial
from itertools import groupby
import json

import logging
_logger = logging.getLogger(__name__)


class ProductPack(models.Model):
	_name = 'product.pack'
	_description = "Product Pack"

	bi_product_template = fields.Many2one(
		comodel_name='product.template', 
		string='Product pack'
	)
	bi_product_product = fields.Many2one(
		comodel_name='product.product', 
		string='Product pack.',
		related='bi_product_template.product_variant_id'
	)
	name = fields.Char(
		related='category_id.name', 
		readonly=True
	)
	is_required = fields.Boolean('Required')
	category_id = fields.Many2one(
		'pos.category',
		'Category',
		required=True
	)
	product_ids = fields.Many2many(
		comodel_name='product.product', 
		string='Product', 
		required=True,
		domain="[('pos_categ_ids','=', category_id)]"
	)
	maxima_cantidad_por_categoria = fields.Integer(
        string='Máxima Cantidad por Categoría',
		required=True,
        help='Define la cantidad máxima permitida por categoría'
    )
	#minima_cantidad_por_categoria = fields.Integer(
	#	string='Mínima Cantidad por Categoría',
	#	required=True,
	#	help='Define la cantidad mínima permitida por categoría'
	#)

	cantidades = fields.Float(
        string='Cantidad usada del producto',
        required=True,
        help='Define la cantidad que se usara de esta categoria, todos deben tener el la misma unidad de medida',
        digits=(8, 6)  # 8 dígitos antes del punto decimal, 6 después
    )

class pos_config(models.Model):
	_inherit = 'pos.config'
	
	use_combo = fields.Boolean('Use combo in POS')
	combo_pack_price = fields.Selection([('all_product', "Total of all combo items "), ('main_product', "Take Price from the Main product")], string='Total Combo Price', default='all_product')


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'


	use_combo = fields.Boolean(related='pos_config_id.use_combo',readonly=False)
	combo_pack_price = fields.Selection(related='pos_config_id.combo_pack_price',readonly=False)

class ProductProduct(models.Model):
	_inherit = 'product.template'

	is_pack = fields.Boolean(string='Is Combo Product')
	pack_ids = fields.One2many(comodel_name='product.pack', inverse_name='bi_product_template', string='Product pack')
	#combo_limitation = fields.Integer(string="Combo Limitation")

class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'

	combo_prod_ids = fields.Many2many("product.product",string="Combo Produts")
	is_pack = fields.Boolean(
		string='Pack',
	)
	combo_products = fields.Char(string="Combo Products")

	def _export_for_ui(self, orderline):
		result = super(PosOrderLine, self)._export_for_ui(orderline)
		result['is_pack'] = orderline.is_pack
		result['combo_prod_ids'] = [orderline.combo_prod_ids.mapped(lambda product: product.id)]

		#result['maxima_cantidad_por_categoria'] = [orderline.combo_prod_ids.mapped(lambda product: product.id)]
		#result['minima_cantidad_por_categoria'] = [
		#	orderline.combo_prod_ids.mapped(
		#		lambda product: product.pack_ids.filtered(
		#			lambda pack: pack.bi_product_product.id == product.id
		#		).mapped('minima_cantidad_por_categoria')
		#	)
		#]
		return result



class POSOrderLoad(models.Model):
	_inherit = 'pos.session'

	def _loader_params_product_product(self):
		result = super()._loader_params_product_product()
		result['search_params']['fields'].extend([
			'is_pack',
			'pack_ids'#,
			#'combo_limitation'
		])
		return result


	def _pos_ui_models_to_load(self):
		result = super()._pos_ui_models_to_load()
		new_model = 'product.pack'
		if new_model not in result:
			result.append(new_model)
		return result

	def _loader_params_product_pack(self):
		return {
			'search_params': {
				'fields': [
					'product_ids', 
					'is_required', 
					'category_id',
					'bi_product_product',
					'bi_product_template',
					'name',
					'maxima_cantidad_por_categoria',
					#'minima_cantidad_por_categoria',
					'cantidades',
				],
			}
		}

	def _get_pos_ui_product_pack(self, params):
		return self.env['product.pack'].search_read(**params['search_params'])
	

class RelatedPosStock(models.Model):
	_inherit = 'stock.picking'

	def _prepare_stock_move_vals_for_sub_product(self, first_line, item, order_lines):		
		cadena = first_line.combo_products 
		# Reemplazar comillas simples por comillas dobles
		cadena = cadena.replace("'", '"')
		cadena = cadena.replace('True', 'true').replace('False', 'false').replace('None', 'null')
		
		array = json.loads(cadena)
		total_combo_qty = 0

		#_logger.info("=entro?========================================================================")
		for product in array:
			try:
				if item.id == product.get('id'):
					if product.get('combo_qty', 0) != product.get('cantidades', 1):
						total_combo_qty +=  first_line.qty * product.get('combo_qty', 0) * product.get('cantidades', 1) 
					else:
						total_combo_qty += product.get('combo_qty', 0) * first_line.qty
					#_logger.info(f"Procesando producto: {product}")
					#_logger.info(f"Erick - combo_qty {product.get('combo_qty', 0)}")
					#_logger.info(f"Erick - cantidades {product.get('cantidades', 1)}")
			except Exception as e:
				_logger.error(f"Error al obtener el campo {field_name}: {e}")
		#_logger.info("=aa========================================================================")
		# Buscar un movimiento existente para el mismo producto
		existing_move = self.env['stock.move'].search([
			('picking_id', '=', self.id),
			('product_id', '=', item.id),
			('state', '=', 'draft')  # Opcional: busca solo movimientos en estado borrador
		], limit=1)

		if existing_move:
			# Actualizar la cantidad del movimiento existente
			existing_move.product_uom_qty += abs(total_combo_qty)
			#_logger.info(f"Actualizado movimiento existente para {item.name}, cantidad total: {existing_move.product_uom_qty}")
			return {
				'name': first_line.name,
				'product_uom': item.uom_id.id,
				'picking_id': self.id,
				'picking_type_id': self.picking_type_id.id,
				'product_id': item.id,
				'product_uom_qty': abs(total_combo_qty),
				'state': 'draft',
				'location_id': self.location_id.id,
				'location_dest_id': self.location_dest_id.id,
				'company_id': self.company_id.id,
			}

		return {
			'name': first_line.name,
			'product_uom': item.uom_id.id,
			'picking_id': self.id,
			'picking_type_id': self.picking_type_id.id,
			'product_id': item.id,
			'product_uom_qty': abs(total_combo_qty),
			'state': 'draft',
			'location_id': self.location_id.id,
			'location_dest_id': self.location_dest_id.id,
			'company_id': self.company_id.id,
		}
					
	def _create_move_from_pos_order_lines(self, lines):
		
		self.ensure_one()
		if not any(line.combo_prod_ids for line in lines):
			return super(RelatedPosStock, self)._create_move_from_pos_order_lines(lines)
		lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
		for product, olines in lines_by_product:
			order_lines = self.env['pos.order.line'].concat(*olines)
			
			#aqui debe hacer un recorrido de order_lines

			#_logger.info("=aa========================================================================")
			#for record in order_lines:
			#	_logger.info(f"Valores del registro con ID {record.id}:")
			#	
			#	for field_name in record._fields:
			#		try:
			#			value = getattr(record, field_name)
			#			_logger.info(f"  {field_name}: {value}")
			#		except Exception as e:
			#			_logger.error(f"Error al obtener el campo {field_name}: {e}")
			#_logger.info("=aa========================================================================")

			#_logger.info("=aa========================================================================")
			#_logger.info(order_lines)
			first_line = order_lines[0]
			current_move = self.env['stock.move'].create(
				self._prepare_stock_move_vals(first_line, order_lines)
			)

			for order_line in order_lines:
				first_line = order_line
				if first_line.combo_prod_ids:
					for item in first_line.combo_prod_ids:
						# Preparar los valores para el movimiento
						prepared_vals = self._prepare_stock_move_vals_for_sub_product(first_line, item, order_lines)
						
						# Buscar un movimiento existente relacionado con el ítem
						existing_move = self.env['stock.move'].search([
							('picking_id', '=', self.id),
							('product_id', '=', item.id),
							('state', '=', 'draft')  # Opcional: busca solo movimientos en estado borrador
						], limit=1)
						
						if existing_move:
							_logger.info("existe")
						else:
							current_move = current_move.create(
								prepared_vals
							)
		self._link_owner_on_return_picking(lines)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
