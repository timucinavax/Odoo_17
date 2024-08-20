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
        const [ products ] = values
        Object.assign(this, { products })
    },
    start: function () {
        this._super(...arguments)
        const refEl = this.$el.find('.products_grid')
        const { products } = this
        console.log(this.$el)
        console.log(products)
//        refEl.html(renderToElement('product_visibility.template_allowed_products', {
//            products
//        }));
    }
});
publicWidget.registry.websiteSaleProducts = websiteSaleProducts