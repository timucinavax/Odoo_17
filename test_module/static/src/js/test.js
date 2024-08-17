/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ChildComp } from "./hello";
import { useRef, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class Counter extends Component {
    static template = "test_module.Counter";
    static components = { ChildComp };

    setup() {
        this.state = useState({ value: 0 , product:''});
        this.orm = useService('orm')
        useEffect(
            () => {
            let product = this.getProductName(this.state.value)
            },
            () => [this.state.value]
        );
    }

    increment() {
        this.state.value++;
    }
    decrement(){
        this.state.value--;
    }
    async getProductName(productId) {
        const product = await this.orm.read('product.template',[productId] ,['name']);

        this.state.product = product[0]['name']
        return product[0]['name']
    }

}
registry.category("actions").add('counter_2',Counter);
