import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App";
import components from "@/components/UI";
import router from "@/router/router";

import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-icons/font/bootstrap-icons.css";

const app = createApp(App);
const pinia = createPinia();

components.forEach(component => {
	app.component(component.name, component);
});

app.use(pinia).use(router).mount("#app");
