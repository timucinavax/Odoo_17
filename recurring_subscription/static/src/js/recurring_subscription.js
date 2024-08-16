/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { registry } from "@web/core/registry";

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
