/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
//import { Layout } from "@web/search/layout";

//export class ProductPrice extends Component {
//    setup() {
//        this.action = useService("action");
//        this.orm = useService("orm")
//    }
//    onChangeProduct(ev) {
//        console.log('--------------')
//        console.log(this)
//        this.renderHtml();
//    }
//}
////ProductPrice.components = { layout };
//ProductPrice.props = {
//    action: { type: Object },
//    "*": true,
//}
//ProductPrice.template = "recurring_subscription.subscription_form";
//registry.category("actions").add("generate_price_of_product", ProductPrice);


//import { patch } from "@web/core/utils/patch";
//import { FormView } from "@web/form/form_view";
//import { FormController } from "@web/form/form_controller";
//import { useService } from "@web/core/utils/hooks";
//
//patch(FormController.prototype, {
//        setup(){
//            super.setup();
//            this.rpc = useService("rpc");
//        },
//        _onChangeProduct(event) {
//            console.log(event);
//        }
//    });


export const WebsiteSubscription = publicWidget.Widget.extend({
    selector: '.oe_website_subscription',
    events: Object.assign({
        'change #product_id': '_onChangeProduct'
    }),
    _onChangeProduct: function (ev) {
            console.log('------------')
            console.log($(this).data))
            },
    });
publicWidget.registry.WebsiteSubscription = WebsiteSubscription
//export class FetchPrice extends Component {
//    static template = 'subscription_form';
//    setup() {
//        function onChangeProduct() {
//            console.log('/////////////');
//        }
//    }
//
//}
//console.log('-----------');
//registry.category("public_components").add('subscription_form', FetchPrice);