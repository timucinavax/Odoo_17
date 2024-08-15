/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { jsonrpc } from "@web/core/network/rpc_service";

export const WebsiteSubscription = publicWidget.Widget.extend({
    selector: '.oe_website_subscription',
    events: Object.assign({
        'change #product_id': '_onChangeProduct'
    }),
    start: function() {
        let product_id = this.$el.find('#product_id').val()
        this._getProductPrice(product_id);
    },
    _onChangeProduct: function (ev) {
        let product_id = $(ev.currentTarget).val();
        this._getProductPrice(product_id);
    },
    _getProductPrice: function(productId) {
        jsonrpc('/get_product_price', {product_id: productId}).then((res) => {
            if (res) {
                this.$el.find('#recurring_amount').val(res);
            }
        })
    }
    });
publicWidget.registry.WebsiteSubscription = WebsiteSubscription;
