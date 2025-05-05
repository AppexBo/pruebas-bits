odoo.define(
    '@pos_loyalty/overrides/components/partner_list_screen/partner_list_screen', 
    [
        '@point_of_sale/app/screens/partner_list/partner_list',
        '@web/core/utils/patch'
    ], 
    function(require) {
        "use strict";

        const { PartnerListScreen } = require("@point_of_sale/app/screens/partner_list/partner_list");
        const { patch } = require("@web/core/utils/patch");

        patch(PartnerListScreen.prototype, {
            get partners() {
                console.log("[Erick] partners - query:", this.state.query || "(vacía)"); // Único console.log añadido
                let res;
                if (this.state.query && this.state.query.trim() !== "") {
                    res = this.pos.db.search_partner(this.state.query.trim());
                } else {
                    res = this.pos.db.get_partners_sorted(1000);
                }
                res.sort(function(a, b) {
                    return (a.name || "").localeCompare(b.name || "");
                });
                if (this.state.selectedPartner) {
                    const indexOfSelectedPartner = res.findIndex( (partner) => partner.id === this.state.selectedPartner.id);
                    if (indexOfSelectedPartner !== -1) {
                        res.splice(indexOfSelectedPartner, 1);
                    }
                    res.unshift(this.state.selectedPartner);
                }
                return res;
            },
        
            _clearSearch() {
                console.log("[Erick] _clearSearch ejecutado"); // Único console.log añadido
                this.searchWordInputRef.el.value = "";
                this.state.query = "";
            },
        
            async searchPartner() {
                console.log("[Erick] searchPartner - query:", this.state.query); // Único console.log añadido
                if (this.state.previousQuery != this.state.query) {
                    this.state.currentOffset = 0;
                }
                const result = await this.getNewPartners();
                this.pos.addPartners(result);
                if (this.state.previousQuery == this.state.query) {
                    this.state.currentOffset += result.length;
                } else {
                    this.state.previousQuery = this.state.query;
                    this.state.currentOffset = result.length;
                }
                return result;
            },
        
            async getNewPartners() {
                console.log("[Erick] getNewPartners - query:", this.state.query); // Único console.log añadido
                let domain = [];
                const limit = 30;
                if (this.state.query) {
                    const search_fields = ["name", "parent_name", "phone", "mobile", "email", "barcode", "street", "zip", "city", "state_id", "country_id", "vat", ];
                    domain = [...Array(search_fields.length - 1).fill('|'), ...search_fields.map(field => [field, "ilike", this.state.query + "%"])];
                }
                const result = await this.orm.silent.call("pos.session", "get_pos_ui_res_partner_by_params", 
                    [odoo.pos_session_id], {
                    domain,
                    limit: limit,
                    offset: this.state.currentOffset
                });
                return result;
            }
        });

        return {};
    }
);