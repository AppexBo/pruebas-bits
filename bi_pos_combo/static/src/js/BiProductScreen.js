/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
	setup() {
		//this.changePos(this.pos);
		super.setup();
	}, 
	/*
	changePos(){
	    const observer = new MutationObserver(() => {            
            
			$("button.button.icon.btn.btn-lg.btn-secondary").each(function() {
				if ($(this).text().trim() === 'Venta diaria') {
					$(this).hide();
				}
			});
			
			$("div.popup.popup-confirm").each(function() {
                if ($(this).find("h4").text().trim() === 'Diferencia de pagos') {
					//simular presionar un boton 
					$(this).find("div.button.confirm.btn.btn-lg.btn-primary").click();
					//ocultar todo
                    $(this).hide();
                }
            });

        });

		observer.observe(document.body, {
            childList: true,
            subtree: true
        });
	},
	*/
    _setValue(val) {
    	const { numpadMode } = this.pos;
    	let self = this;
		let order = this.currentOrder;
		if(this.currentOrder.get_selected_orderline()){
			if(this.currentOrder.get_selected_orderline().product.is_pack){
				if(numpadMode==='quantity'){
					var orderline = order.get_selected_orderline()
					if (val === "remove") {
	                    this.currentOrder.removeOrderline(orderline);
	                }else{
	                	orderline.set_quantity(val,'keep_price')
	                } 

				}else{
					super._setValue(val);
				}
			}	
			else{
				super._setValue(val);
			}
		} 
    }
});