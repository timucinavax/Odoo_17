/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ChildComp } from "./hello";

export class Counter extends Component {
    static template = "test_module.Counter";
    static components = { ChildComp };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
    decrement(){
        this.state.value--;
    }
}
registry.category("actions").add('counter_2',Counter);
