/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
// import { jsonrpc } from "@web/core/network/rpc_service";
// import { registry } from "@web/core/registry";

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, useState } from "@odoo/owl";
//import { getOperationsTypes } from "@l10n_py_point_sale/static/src/js/models";

patch(PartnerDetailsEdit.prototype, {
    setup() {
        super.setup(...arguments);
        this.py_pos = usePos();
        const partner = this.props.partner;
        this.intFields = ["l10n_latam_identification_type_id", "operation_type_id", 'distrit_id', 'locality_id'];

        // Lista de opciones para receiver_nature
        this.receiverNatureOptions = [
            ['1', "(1) Contribuyente"],
            ['2', "(2) No contribuyente"]
        ];
        
        this.taxpayer_type_options = [
            ['1', "Persona Física"],
            ['2', "Persona Jurídica"]
        ];
        

        //Establecer el valor inicial si existe en el partner
        this.changes.l10n_latam_identification_type_id = this.getDefaultIdentificationType(partner);
        this.changes.operation_type_id = this.getDefaultOperationType(partner);
        this.changes.distrit_id = this.props.partner.distrit_id && this.props.partner.distrit_id[0];
        this.changes.locality_id = this.props.partner.locality_id && this.props.partner.locality_id[0];
        this.changes.receiver_nature = this.getDefaultReceiverNature(partner); //this.props.partner.receiver_nature || this.receiverNatureOptions[0][0];
        this.changes.taxpayer_type = this.getDefaultTaxpayerType(partner); //this.props.partner.taxpayer_type || '';
        this.changes.house_number = this.props.partner.house_number;
        // this.changes = useState(
        //     {
        //         //l10n_latam_identification_type_id : this.props.partner.l10n_latam_identification_type_id && this.props.partner.l10n_latam_identification_type_id[0],
        //         operation_type_id : this.getDefaultOperationType(partner),
        //         // distrit_id : this.props.partner.distrit_id && this.props.partner.distrit_id[0],
        //         // locality_id : this.props.partner.locality_id && this.props.partner.locality_id[0],
        //         //receiver_nature : partner.receiver_nature || this.receiverNatureOptions[0][0],
        //         // taxpayer_type : this.props.partner.taxpayer_type || '',
        //         // house_number : this.props.partner.house_number,
                
        //     }
        // )
    },

    getDefaultOperationType(partner) {
        if (partner.operation_type_id && partner.operation_type_id[0]){
            return partner.operation_type_id && partner.operation_type_id[0];
        }
        if (this.py_pos.default_operation_type_id){
            var default_operation_type_id = this.py_pos.default_operation_type_id;
            return default_operation_type_id;
        }
        return false;
    },

    getDefaultIdentificationType(partner) {
        if (partner.l10n_latam_identification_type_id && partner.l10n_latam_identification_type_id[0]){
            return partner.l10n_latam_identification_type_id && partner.l10n_latam_identification_type_id[0];
        }
        if (this.py_pos.default_identification_type_id){
            return this.py_pos.default_identification_type_id;
        }
        return false;
    },
    
    getDefaultReceiverNature(partner){
        if (partner.receiver_nature){
            return partner.receiver_nature;
        }
        if (this.py_pos.default_receiver_nature){
            return this.py_pos.default_receiver_nature;
        }
        return false;
    },

    getDefaultTaxpayerType(partner){
        if (partner.taxpayer_type){
            return partner.taxpayer_type;
        }
        if (this.py_pos.default_taxpayer_type){
            return this.py_pos.default_taxpayer_type;
        }
        return false;
    },
    

    saveChanges() {
        return super.saveChanges(...arguments);
    },
});
