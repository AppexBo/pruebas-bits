/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { SelectComboProductPopupWidget } from "@bi_pos_combo/js/SelectComboProductPopupWidget";
import { roundDecimals as round_di } from "@web/core/utils/numbers";

patch(PosStore.prototype, {
    // @Override
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.product_pack = loadedData['product.pack'] || [];
        // this.db.line_combo_prod = {};
    },
    async addProductToCurrentOrder(product, options = {}) {    	
    	var self = this;
    	let order = this.get_order();
    	if(product.to_weight && this.config.iface_electronic_scale){
    		this.gui.show_screen('scale',{product: product});
    	}else{
    		if(product.is_pack){
				var required_products = [];
				var optional_products = [];
				var all_categories = [];
				var combo_products = self.product_pack;
				if(combo_products){
					var existe_algun_producto_sin_categoria=false;
					for (var i = 0; i < combo_products.length; i++) {
						if(combo_products[i]['bi_product_product'][0] == product['id'])
						{
							combo_products[i]['product_ids'].forEach(function (prod) {
								var sub_product = self.db.get_product_by_id(prod);
								if(sub_product){
									if(combo_products[i]['is_required'])
									{
										sub_product['combo_qty'] = combo_products[i]['cantidades'];
										sub_product['maxima_cantidad_por_categoria'] = combo_products[i]['maxima_cantidad_por_categoria'];
										//sub_product['minima_cantidad_por_categoria'] = combo_products[i]['minima_cantidad_por_categoria'];
										sub_product['combo_product_category_id'] = combo_products[i]['category_id'];
										sub_product['cantidades'] = combo_products[i]['cantidades'];
										required_products.push(sub_product)
									}
									else{
										sub_product['combo_qty'] = 0;
										sub_product['maxima_cantidad_por_categoria'] = combo_products[i]['maxima_cantidad_por_categoria'];
										//sub_product['minima_cantidad_por_categoria'] = combo_products[i]['minima_cantidad_por_categoria'];
										sub_product['combo_product_category_id'] = combo_products[i]['category_id'];
										sub_product['cantidades'] = combo_products[i]['cantidades'];
										
										if (!all_categories.some(category => category.id === sub_product['combo_product_category_id'][0])) {
											all_categories.push(
												{
													id: sub_product['combo_product_category_id'][0], 
													name: sub_product['combo_product_category_id'][1]
												}
											);
										}

										optional_products.push(sub_product)
									}
								}else{
									existe_algun_producto_sin_categoria=true;
								}
							});
						}
					}
					if(existe_algun_producto_sin_categoria){
						alert("Por revisa los productos ya que no tiene asignado una categoría.")
					}
				}
				if(required_products.length > 0 || optional_products.length > 0){
					self.env.services.pos.popup.add(SelectComboProductPopupWidget, {'product': product,'required_products':required_products,'optional_products':optional_products, 'all_categories': all_categories , 'update_line' : false });
				}	
	                	
			}
			else{
				super.addProductToCurrentOrder(product, options = {});
			}
		}
    },
});

patch(Orderline.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.pos   = options.pos;
		this.order = options.order;
		var self = this;
		if (options.json) {
			this.init_from_JSON(options.json);
			return;
		}
		this.combo_products = this.combo_products;
		var final_data = self.pos.final_products;
		if(final_data){
			for (var i = 0; i < final_data.length; i++) {
				if(final_data[i] == undefined){
					i=i+1;
					if(final_data[i][0] == this.product.id){
						var combo_list = self.prepare_combo_list(final_data[i][0])
						this.combo_products = final_data[i][1];
						self.pos.final_products = null;
					}
				}
				else{
					if(final_data[i][0] == undefined){
						return;
					}
					if(final_data[i][0] == this.product.id){
						this.combo_products = final_data[i][1];
						self.pos.final_products = null;
					}
				}
			}
		}
		this.set_combo_products(this.combo_products);
		this.combo_prod_ids =  this.combo_prod_ids || [];
		this.is_pack = false;
    },
    prepare_combo_list(list_data){
    	var combo_data=[];
    	list_data.forEach(function(data){
    		if(data != null){
	    		var prod_data =  {
							'active': data.active,
							'applicablePricelistItems': data.applicablePricelistItems,
							'attribute_line_ids' : data.attribute_line_ids,
							'available_in_pos': data.available_in_pos,
							'barcode': data.barcode,
							'categ': data.categ,
							'categ_id': data.categ_id,
							'cid': data.cid,
							'combo_qty': data.combo_qty,
							'cantidades': data.cantidades,
							'combo_limit': data.combo_limit,
							'default_code': data.default_code,
							'description': data.description,
							'description_sale': data.description_sale,
							'display_name': data.display_name,
							'id': data.id,
							'lst_price': data.lst_price,
							'is_pack': data.is_pack,
							'pack_ids': data.pack_ids,
							'standard_price': data.standard_price,
							'taxes_id': data.taxes_id,
							'type': data.type,
							'image_128': data.image_128,
							'invoice_policy': data.invoice_policy,
							'optional_product_ids': data.optional_product_ids,
							'parent_category_ids': data.parent_category_ids,
							'pos_categ_id': data.pos_categ_id,
							'product_image_url': data.product_image_url,
							'product_tmpl_id': data.product_tmpl_id,
							'to_weight': data.to_weight,
							'tracking': data.tracking,
							'uom_id': data.uom_id,
							"__last_update": data.__last_update
						}

					combo_data.push(prod_data)
			}
			
    	});
    	return combo_data


    },
    on_click(){
	    var pack_product = this.env.services.pos
        var product = this.product
		var required_products = [];
		var optional_products = [];
		var combo_products = pack_product.product_pack;
		
        if(product)
		{
			for (var i = 0; i < combo_products.length; i++) {
				if(combo_products[i]['bi_product_product'][0] == product['id'])
				{
					if(combo_products[i]['is_required'])

					{
						
						combo_products[i]['product_ids'].forEach(function (prod) {
							var sub_product = product.pos.db.get_product_by_id(prod);
							required_products.push(sub_product)
						});
					}
					else{
						combo_products[i]['product_ids'].forEach(function (prod) {
							var sub_product = product.pos.db.get_product_by_id(prod);
							optional_products.push(sub_product)
						});
					}
				}
			}
		}
		this.env.services.pos.popup.add(SelectComboProductPopupWidget, {'product': product,'required_products':required_products,'optional_products':optional_products , 'update_line' : true });
	},
	getDisplayData() {
        return {
            ...super.getDisplayData(),
            is_pack : this.is_pack,
			price_manually_set : this.price_manually_set,
			combo_prod_ids : this.combo_prod_ids || [],
			combo_products : this.combo_products,
        };
    },
	init_from_JSON(json){
		super.init_from_JSON(...arguments);
		var self = this;
		
		if(json.combo_prod_ids){
			this.combo_prod_ids = json.combo_prod_ids[0];
			this.combo_products = this.get_combo_products();
			this.set_combo_products(this.combo_products);
		}
		else{
			this.combo_products = [];
			this.combo_prod_ids = [];
		}
		
		this.is_pack = json.is_pack;
	},
	export_as_JSON(){
		const json = super.export_as_JSON(...arguments);
		json.combo_products = this.combo_products;
		json.combo_prod_ids= this.combo_prod_ids;
		json.is_pack=this.is_pack;
		
		return json;
	},
	export_for_printing(){
		const json = super.export_for_printing(...arguments);
		json.combo_products = this.combo_products;
		json.combo_prod_ids= this.combo_prod_ids;
		json.is_pack=this.is_pack;
		return json;
	},
	set_combo_prod_ids(ids){
		this.combo_prod_ids = ids
	},
	set_combo_products(products){
		var ids = [];
		if(this.product.is_pack)
		{	
			if(products)
			{
				products.forEach(function (prod) {
					if(prod != null)
					{
						ids.push(prod.id)
					}
				});
			}
			var list_data = this.prepare_combo_list(products)
			this.combo_products = list_data;
			this.set_combo_prod_ids(ids)
			if(this.combo_prod_ids)
			{
				this.set_combo_price(this.price);
			}
		}

	},
	set_is_pack(is_pack){
		this.is_pack = is_pack
	},
	set_unit_price(price){
		var self = this;
		this.order.assert_editable();
		this.set_is_pack(true);
		if(this.combo_products && self.pos.config.combo_pack_price == 'all_product'){
			var prods = this.combo_products;
			var total = 0;
			prods.forEach(function (prod) {
				if(prod)
				{
					total += prod.lst_price	
				}	
			});
			this.price = round_di(parseFloat(total) || 0, this.pos.dp['Product Price']);
		}
		else{
			this.price = round_di(parseFloat(price) || 0, this.pos.dp['Product Price']);
		}
	},
	set_combo_price(price){
		var self = this;
		var prods = this.get_combo_products()
		var total = 0;
		prods.forEach(function (prod) {
			if(prod)
			{
				total += prod.lst_price	* prod.combo_qty
			}	
		});
		if(self.pos.config.combo_pack_price== 'all_product'){
			this.set_unit_price(total);
		}
		else{
			let prod_price = this.product.lst_price;
			this.set_unit_price(prod_price);
		}
	},
	
	get_combo_products(){
		var self = this;
		if(this.product.is_pack)
		{
			var get_sub_prods = [];
			if(this.combo_products)
			{
				return this.combo_products
			}
			if(this.combo_prod_ids)
			{
				this.combo_prod_ids.forEach(function (prod) {
					var sub_product = self.pos.db.get_product_by_id(prod);
					get_sub_prods.push(sub_product)
				});
				return get_sub_prods;
			}
		}
	}
});




patch(Order.prototype, {
	setup() {
        super.setup(...arguments);
		this.barcode = this.barcode || "";
	},
	// set_partner(partner) {
    //     this.assert_editable();
    //     this.partner = partner;
    // }

});
