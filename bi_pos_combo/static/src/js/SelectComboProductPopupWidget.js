/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { Component, onMounted, useRef } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SelectComboProductPopupWidget extends AbstractAwaitablePopup {
    static template = "bi_pos_combo.SelectComboProductPopupWidget";

    setup() {
		super.setup();
		this.pos = usePos();
		onMounted(() =>{
			var self = this;
			var order = self.pos.get_order();
			if(order){
				var orderlines = order.get_orderlines();
				this.product = self.props.product;
				this.update_line = self.props.update_line;
				this.required_products = self.props.required_products;
				this.optional_products = self.props.optional_products;
				this.combo_products = self.pos.pos_product_pack;
				
				$('.optional-product').each(function(){
					if(self.update_line){
	                    var selectedprod = parseInt(this.dataset.productId);
	                    var order = self.pos.get_order();
	                    var selected_orderline = order.get_selected_orderline()
	                    if(order){
	                        if (selected_orderline) {
	                            if(selected_orderline.product.id == self.props.product.id){
	                                var selected_product = selected_orderline.combo_prod_ids
	                                var combo_products = self.pos.pos_product_pack;
	                                for (var i = 0; i < selected_product.length; i++){

	                                    if(selected_product[i] == selectedprod){
	                                        $(this).addClass('raghav');
	                                    }
	                                };
	                            }
	                        }
	                    }
	                }
				});
			}
		});
	}
	go_back_screen() {
		this.pos.showScreen('ProductScreen');
		this.cancel();
		//debugger
	}
	update_produc(id,qty){
		$("#"+id).each(function(){
			if(self.update_line){
				$(this).on('click',function () {
                    if($(this).hasClass('raghav')){
                    	$(this).removeClass('raghav');
                    }else{
                    	$(this).addClass('raghav');
                    }
				});
                var selectedprod = parseInt(this.dataset.productId);
                var order = self.pos.get_order();
                var selected_product = order.get_selected_orderline()
                if(order){
                    if (order.get_selected_orderline()) {
                        if(order.get_selected_orderline().product.id == self.props.product.id){
                            var selected_product = order.get_selected_orderline().combo_prod_ids
                            var combo_products = self.pos.pos_product_pack;
                            for (var i = 0; i < selected_product.length; i++){

                                if(selected_product[i] == selectedprod){
                                    $(this).addClass('raghav');
                                }
                            };
                        }
                    }
                }
            }
            else{
				if(qty > 0){
					if(! $(this).hasClass('raghav') ){
                    	$(this).addClass('raghav');
                    }
				}else{
					if($(this).hasClass('raghav') ){
                    	$(this).removeClass('raghav');
                    }
				}

            }
		});
	}

	update_optional_product_by_id(id,qty){
		var self = this
		const currentProduct = this.props.optional_products.find(prd => prd.id === id);
		
		// Buscar el producto actual para obtener su combo_product_category_id
		const categoryId = currentProduct.combo_product_category_id;
		if (!currentProduct) {
			console.warn("Producto no encontrado.");
			return;
		}
		// Sumar los combo_qty de productos con la misma categoría
		let totalSumados = 0;
		this.props.optional_products.forEach(prd => {
			//debugger
			if (prd.combo_product_category_id === categoryId) {
				totalSumados += prd.combo_qty || 0; // Asegurarse de que combo_qty tenga un valor numérico
			}
		});

		const newTotal = totalSumados - (currentProduct.combo_qty || 0) + qty;
		
		// Validar si la cantidad excede el límite
		if (newTotal > currentProduct.maxima_cantidad_por_categoria) {
			alert("Límite de productos de categoría excedido.");
		} else {
			// Actualizar la cantidad del producto
			currentProduct.combo_qty = qty;
			self.update_produc(id, qty);
		}

		/*$.each(this.props.optional_products, function( i, prd ){
			debugger
			//aqui un foreach de los productos para validar la cantidad
			//tengo q saber la categoria combo_product_category_id
			if(prd.id == id){
				if( qty > newTotal ){
					alert("Límite de productos excedido.")
				}else{
					prd['combo_qty'] = qty
					self.update_produc(id,qty)
				}
			}
		});*/
		
	}

	AddQty(event) {
		var self = this;
		var currentProductId = parseInt(event.currentTarget.dataset['productId'])
	
		$(".qty-label").each(function( index ) {
			var prd_id_qty = parseInt($(this).attr('product-id'));
			var product = self.pos.db.get_product_by_id(prd_id_qty);
			if (currentProductId == prd_id_qty){
				let added_qty = parseInt($(this).text()) + 1
				if(added_qty <= product.combo_limit){
					$(this).text(added_qty);
				}
				self.update_optional_product_by_id(prd_id_qty,added_qty)

			}
		});
	}

	MinusQty(event) {
		var self = this;
		var currentProductId = parseInt(event.currentTarget.dataset['productId'])
		$(".qty-label").each(function( index ) {
			var prd_id_qty = parseInt($(this).attr('product-id'));
			var product = self.pos.db.get_product_by_id(prd_id_qty);
			if (currentProductId == prd_id_qty){
				if (parseInt($(this).text()) > 0){
					$(this).text(parseInt($(this).text()) - 1);
					self.update_optional_product_by_id(prd_id_qty,parseInt($(this).text()))
				}
			}
		});
	}

	get req_product() {
		let req_product = [];
		$.each(this.props.required_products, function( i, prd ){
			prd['product_image_url'] = `/web/image?model=product.product&field=image_128&id=${prd.id}&write_date=${prd.write_date}&unique=1`;
			req_product.push(prd)
		});
		return req_product;
	}

	get optional_product(){
		let optional_product = [];
		$.each(this.props.optional_products, function( i, prd ){
			prd['product_image_url'] = `/web/image?model=product.product&field=image_128&id=${prd.id}&write_date=${prd.write_date}&unique=1`;
			optional_product.push(prd)
		});
		return optional_product;
	}


		
	renderElement() {
		var self = this;
		var order = self.pos.get_order();
		if(order){
			var orderlines = order.get_orderlines();
			var final_products = this.required_products;
			$('.remove-product').click(function(ev){
				ev.stopPropagation();
				ev.preventDefault();
				var prod_id = parseInt(this.dataset.productId);
				$(this).closest(".optional-product").hide();
				for (var i = 0; i < self.props.optional_products.length; i++)
				{
					if(self.props.optional_products[i]['id'] == prod_id)
					{
						self.props.optional_products.splice(i, 1);
					}
				}
			});
		}
	}
	add_confirm(ev){
		var final_products = this.props.required_products;
		var order = this.pos.get_order();
		var selected_orderline = order.get_selected_orderline();
		ev.stopPropagation();
		ev.preventDefault();
		var self = this   
		$('.raghav').each(function(){
			var prod_id = parseInt(this.dataset.productId);
			for (var i = 0; i < self.props.optional_products.length; i++) 
			{
				if(self.props.optional_products[i]['id'] == prod_id)
				{
					final_products.push(self.props.optional_products[i]); 
				}
			}
			
		});
		var add = [];
		var new_prod = [self.props.product.id,final_products];
		
		/*if(self.pos.final_products)
		{
			add.push(self.env.pos.pos_product)
			add.push(new_prod)
			self.pos.final_products = add;
		}
		else{
			add.push(new_prod)
			self.pos.final_products = add;
		}*/
		add.push(new_prod);
		self.pos.final_products = add;
		
		if(self.props.update_line){
		
            if(selected_orderline != null){
                selected_orderline.set_combo_products(final_products)
            }
            else{
                //order.add_product(self.props.product);
				order.add_product(self.props.product, { merge: false });  // Añadir sin agrupar
            }

		}else{
			//order.add_product(self.props.product)
			order.add_product(self.props.product, { merge: false });  // Añadir sin agrupar
		}
		self.cancel();
	}

}

