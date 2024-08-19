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

var lastFourCredits = publicWidget.Widget.extend({
        selector: '.last_four_credit_snippet',
        willStart: async function () {
            const credits = await jsonrpc('/last_four_credits', {})
            Object.assign(this, {
                credits
            })
        },
        start: function () {
            this._super(...arguments)
            const refEl = this.$el.find("#last_four_credits")
            const { credits } = this
            refEl.html(renderToElement('recurring_subscription.last_four_credit', {
                credits
            }))
        }
    });
publicWidget.registry.lastFourCredits = lastFourCredits;