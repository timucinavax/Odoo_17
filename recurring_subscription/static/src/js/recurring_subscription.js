/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { registry } from "@web/core/registry";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

export const WebsiteSubscription = publicWidget.Widget.extend({
    selector: '.oe_website_subscription',
    events: Object.assign({
        'change #product_id': '_onChangeProduct'
    }),
    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },
    start: function() {
        this._super(...arguments);
        let product_id = this.$el.find('#product_id').val();
        this._getProductPrice(product_id);
    },
    _onChangeProduct: function (ev) {
        let product_id = $(ev.currentTarget).val();
        this._getProductPrice(product_id);
    },
    _getProductPrice: async function(productId) {
       const price = await this.orm.read('product.product', [parseInt(productId)], ['list_price']);
       this.$el.find('#recurring_amount').val(price[0]['list_price']);
    }
    });
publicWidget.registry.WebsiteSubscription = WebsiteSubscription;

//export const creditSnippet = publicWidget.Widget.extend({
//    selector: '.oe_rec_sub_credits',
//    start: function() {
//        this._super(...arguments);
//        let partner_id = this.$el.find('#product_id').val();
//        this.get_credit_record();
//    },
//    get_credit_record() {
//
//    }
//    }
//publicWidget.registry.creditSnippet = creditSnippet;


export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var TopSellingProducts = PublicWidget.Widget.extend({
        selector: '.best_seller_product_snippet',
        willStart: async function () {
            const data = await jsonrpc('/top_selling_products', {})
            const [products, categories, website_id, unique_id] = data
            Object.assign(this, {
                products, categories, website_id, unique_id
            })
        },
        start: function () {
            const refEl = this.$el.find("#top_products_carousel")
            const { products, categories, current_website_id, products_list} = this
            const chunkData = chunk(products, 4)
            refEl.html(renderToElement(recurring_subscription.products_category_wise', {
                products,
                categories,
                current_website_id,
                products_list,
                chunkData
            }))
        }
    });
PublicWidget.registry.products_category_wise_snippet = TopSellingProducts;
return TopSellingProducts;