/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
		//Cambios en el POS
        this.changePos(this.pos);
	}, 

    changePos(pos){
        // Crear un MutationObserver para observar cambios en el DOM
        const observer = new MutationObserver(() => {            
            this.hide_info_button_products_pdv();
            this.hide_zone_pdv();
            this.hide_zone_form_cliente();
            //this.add_acction_button_facturate_detection();
            this.hide_button_venta_diaria_cerrar_sesion();
            this.hide_button_ordenes_menu();
            this.hide_button_numpad_and_others();
            this.hide_all_products_price_eq_cero();
        });
        
        // Observar cambios en el DOM dentro del contenedor principal
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    hide_all_products_price_eq_cero(){
        // Seleccionar todas las etiquetas <article> con la clase especificada
        const articles = document.querySelectorAll(
            'article.flex-column.product.position-relative.btn.btn-light.d-flex.align-items-stretch.p-0.m-0.text-start.cursor-pointer.overflow-hidden.transition-base'
        );

        // Recorrer cada <article>
        articles.forEach(article => {
            // Buscar el <div> con clase "product-content d-flex flex-column justify-content-between h-100 mx-2.py-1"
            const productContent = article.querySelector(
                'div.product-content.d-flex.flex-column.justify-content-between.h-100.mx-2.py-1'
            );

            if (productContent) {
                // Buscar el <span> dentro de este <div>
                const priceTag = productContent.querySelector('span.price-tag.text-primary.py-1.fw-bolder');

                // Verificar si el <span> existe y si su texto comienza con "0" osea los guarani no pueden ser menores a 0
                if (priceTag && priceTag.textContent.trim().startsWith("0")) {
                    // Ocultar el <article> utilizando !important
                    article.style.setProperty('display', 'none', 'important');
                }
            }
        });
    },

    hide_button_venta_diaria_cerrar_sesion(){
        $("button.button.icon.btn.btn-lg.btn-secondary").each(function() {
            if ($(this).text().trim() === 'Venta diaria') {
                $(this).hide();
            }
        });
    },

    hide_button_ordenes_menu(){
        // Seleccionar todos los elementos con la clase "dropdown-item.with-badge.py-2"
        const button_ordenes_menu = document.querySelectorAll(".dropdown-item.with-badge.py-2");
        // Ocultar los elementos encontrados
        button_ordenes_menu.forEach(button_ordenes_menu => {
            // Verificar tiene el campo esta visible
            const have_styles = button_ordenes_menu.hasAttribute('style');
            if (!have_styles) {
                button_ordenes_menu.setAttribute('style', 'display: none !important;')
            }
        });
    },

    hide_button_numpad_and_others(){
        // Seleccionar todos los elementos con la clase ".col.btn.btn-light.py-3.border.fw-bolder.rounded-0"
        const buttons_numpad_and_others = document.querySelectorAll(".col.btn.btn-light.py-3.border.fw-bolder.rounded-0");
        // Lista de valores que deseas ocultar
        const valuesToHide = ["+/-", ",", "% de desc.", "Precio"];
        // Ocultar los elementos encontrados
        buttons_numpad_and_others.forEach(button => {
            if (valuesToHide.includes(button.textContent.trim())) {
                // Verificar tiene el campo esta visible
                const have_styles = button.hasAttribute('style');
                if (!have_styles) {
                    button.setAttribute('style', 'display: none !important;')
                    /*
                    // Ocultar el texto aplicando estilos CSS
                    button.style.color = 'transparent';
                    button.style.textShadow = '0 0 0 transparent';
                    
                    // Bloquear el botón para que no se pueda presionar
                    button.setAttribute('disabled', 'true');
                    */ 
                }
            }
        });
    },

    hide_info_button_products_pdv(){
        // Seleccionar todos los elementos con la clase "product-information-tag"
        const info_buttons = document.querySelectorAll(".product-information-tag");
        // Ocultar los elementos encontrados
        info_buttons.forEach(info_button => {
            // Verificar tiene el campo esta visible
            const have_styles = info_button.hasAttribute('style');
            if (!have_styles) {
                info_button.setAttribute('style', 'display: none !important;')
            }
        });
    },

    hide_zone_pdv(){
        // Seleccionar todos los elementos con la clase "product-information-tag"
        const buttons = document.querySelectorAll(".control-button.btn.btn-light.rounded-0.fw-bolder");
        // Ocultar los elementos encontrados
        buttons.forEach(button => {
            //ocultar unicamente Reembolso
            if(button.textContent.trim() === "Reembolso"){
                button.setAttribute('style', 'display: none !important;')
            }
            //ocultar unicamente Nota de cliente
            if(button.textContent.trim() === "Nota de cliente"){
                button.setAttribute('style', 'display: none !important;')
            }
            //ocultar unicamente Nota de cliente
            if(button.textContent.trim() === "Cotización/orden"){
                button.setAttribute('style', 'display: none !important;')
            }
        });
    },
    hide_zone_form_cliente(){
        // Lista de campos que quieres buscar
        const camposOcultar = [
            "Calle",
            "Ciudad",
            "Código postal",
            "Celular",
            "Código de barras"
        ];
        // Seleccionar todos los div con clase "partner-detail col"
        const divs = document.querySelectorAll("div.partner-detail.col");
        // Iterar sobre cada div
        divs.forEach(div => {
            // Buscar dentro del div si contiene algún label con el texto especificado
            const contieneTexto = Array.from(div.querySelectorAll("label"))
                .some(label => camposOcultar.includes(label.textContent.trim()));
            
            // Si el div contiene un label con el texto, de camposOcultar
            if (contieneTexto) {
                div.setAttribute('style', 'display: none !important;');
            }
        });
    },

    add_acction_button_facturate_detection(){
        const product_screen = document.querySelector('.product-screen');
        if(product_screen){
            const buttons = document.querySelectorAll(
                '.btn-switchpane.btn.flex-fill.rounded-0.fw-bolder.btn-primary, ' +
                '.pay.validation.pay-order-button.btn-primary.button.btn.d-flex.flex-column.flex-fill.align-items-center.justify-content-center.fw-bolder.btn-lg.rounded-0'
            );
    
            // Añadimos un evento de clic a cada botón encontrado
            buttons.forEach(button => {
                button.addEventListener('click', function () {
                    const detect_change = new MutationObserver(() => {            
                        const payment_screen = document.querySelector('.payment-screen');
                        if(payment_screen){
                            const button = document.querySelector('.js_invoice');
                            // Verifica si el botón existe y no tiene las clases "highlight" o "text-bg-primary"
                            if (button && !button.classList.contains('highlight') && !button.classList.contains('text-bg-primary')) {
                                console.log("simulate click");
                                button.click();
                            }
                            //ocultar el boton siempre
                            if(button){
                                console.log("simulate hide");
                                button.setAttribute('style', 'display: none !important;');
                            }
                        }
                    });
                    
                    // Observar cambios en el DOM dentro del contenedor principal
                    detect_change.observe(document.body, {
                        childList: true,
                        subtree: true
                    });
                });
            });
        }
    }

});