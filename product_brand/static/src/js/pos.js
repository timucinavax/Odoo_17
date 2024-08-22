/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";;
console.log('===========')

patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
        console.log(this)
        this.product_temp = loadedData["product.template"];
        console.log(this.product_temp)
    }
})