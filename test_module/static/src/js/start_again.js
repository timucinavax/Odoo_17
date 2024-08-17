/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Counter } from "./test";

export class StartAgain extends Counter {
    static template = 'test_module.start_again'
}
registry.category("actions").add('start_again',StartAgain);




