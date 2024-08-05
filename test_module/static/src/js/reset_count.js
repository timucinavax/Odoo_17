import { Counter } from "./test";
import { patch } from "@web/core/utils/patch";

patch(Counter.prototype, {
    reset(){
        this.state.value = 0;
    },
});