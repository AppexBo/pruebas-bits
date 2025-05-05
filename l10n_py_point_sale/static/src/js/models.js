/** @odoo-module */

import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";



patch(PosStore.prototype, {
    // @Override
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.l10n_latam_identification_types = loadedData['l10n_latam.identification.type'];    
        this.operation_types = loadedData['l10n.py.operation.type'];    
        this.city_ids = loadedData['res.city'];    
        this.locality_ids = loadedData['l10n.py.locality'];    
        this.default_operation_type_id = loadedData['operation_type_id']
        this.default_identification_type_id = loadedData['identification_type_id']
        this.default_receiver_nature = loadedData['receiver_nature']
        this.default_taxpayer_type = loadedData['taxpayer_type']
        this.pos_payment_ref = loadedData['pos.payment'];
        
    },
});