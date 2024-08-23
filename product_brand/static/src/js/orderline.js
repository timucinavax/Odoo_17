//** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";
//patch order line for adding new field in order line
patch(Orderline.prototype, {
    getDisplayData() {
    //overwrite existing function to get data to display to add brand name to data
        return {
            ...super.getDisplayData(),
            brand_name: this.getBrandName(),
        };
    },
    getBrandName() {
    // return brand name of current order line product
        return this.product.brand_id[1]
    },
});
