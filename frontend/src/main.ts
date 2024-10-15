import { createApp } from 'vue';
import "./input.css";
import "primeicons/primeicons.css";
import App from "./App.vue";

import PrimeVue from 'primevue/config';
import Tooltip from 'primevue/tooltip';
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Badge from "primevue/badge";
import FloatLabel from "primevue/floatlabel";
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';

// @ts-ignore
import Aura from './presets/aura';
import router from "./router.ts";
import store from "@/store";

const app = createApp(App);
app.use(PrimeVue, {
    unstyled: true,
    pt: Aura,
});
app.use(store);
app.use(router);

app.directive('tooltip', Tooltip);

app.component("Avatar", Avatar)
app.component('Badge', Badge);
app.component("Button", Button)
app.component("InputText", InputText)
app.component("Message", Message)
app.component('FloatLabel', FloatLabel);
app.component("Splitter", Splitter)
app.component("SplitterPanel", SplitterPanel)

app.mount("#app");