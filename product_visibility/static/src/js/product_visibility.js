/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { registry } from "@web/core/registry";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

export const websiteSaleProducts = publicWidget.Widget.extend({
    selector: '.o_wsale_products_page',
    willStart : async function () {
        this._super(...arguments)
        const values = await jsonrpc('/get_allowed_products', {})
//        console.log(values)
        const { products } = values
//        console.log(products)
        Object.assign(this, { products })
    },
    start: function () {
        this._super(...arguments)
        const refEl = this.$el.find('.products_grid')
//        console.log(this.$el.find('.products'))
//        const { products } = this
//        this.$el.find('.oe_product').hide()
//        this.$el.find('.oe_product[data-product-id="'+47+'"]').show();
//        this.values.forEach(function(product){
//            console.log(el)
//            console.log(product)
//            this.$el.find('.oe_product[data-product-id="'+product.id+'"]').show();
//        })
//        refEl.html(renderToElement('website_sale.products', {
//            products
//        }));
    }
});
publicWidget.registry.websiteSaleProducts = websiteSaleProducts