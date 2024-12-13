import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Badge from "primevue/badge";
import FloatLabel from "primevue/floatlabel";
import Ripple from 'primevue/ripple';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Textarea from "primevue/textarea";

import "@/assets/base.css";
import "primeicons/primeicons.css";

import {app} from '@/appInstance';
import store from "@/store";
import router from "@/router";
import setupInterceptors from "@/services/setupInterceptors";

setupInterceptors();
app.use(PrimeVue, {ripple: true, theme: 'none'});
app.use(ToastService);
app.use(store);
app.use(router);

app.directive('ripple', Ripple);
app.directive('tooltip', Tooltip);

app.component("Avatar", Avatar)
app.component('Badge', Badge);
app.component("Button", Button);
app.component("Dialog", Dialog);
app.component("InputText", InputText);
app.component("Message", Message);
app.component('FloatLabel', FloatLabel);
app.component("Splitter", Splitter);
app.component("SplitterPanel", SplitterPanel);
app.component("Textarea", Textarea);

app.mount("#app");
