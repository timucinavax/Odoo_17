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


export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var TopSellingProducts = publicWidget.Widget.extend({
        selector: '.best_seller_product_snippet',
        willStart: async function () {
            const data = await jsonrpc('/top_selling_products', {})
            const [credit_ids] = data
            Object.assign(this, {
                credit_ids
            })
        },
        start: function () {
            const refEl = this.$el.find("#last_four_credits")
            const { credit_ids } = this
            const chunkData = chunk(credit_ids, 4)
            console.log(chunkData)
            console.log(credit_ids)
            refEl.html(renderToElement('recurring_subscription.products_category_wise', {
                credit_ids,
                chunkData
            }))
        }
    });
publicWidget.registry.TopSellingProducts = TopSellingProducts;