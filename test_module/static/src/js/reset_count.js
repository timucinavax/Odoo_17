/** @odoo-module **/
console.log()
import { patch } from "@web/core/utils/patch";
import { Counter } from './test'

patch(Counter.prototype, {
    reset() {
        this.state.value = 0;
    },
});