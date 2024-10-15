import {createRouter, createWebHistory} from "vue-router";

import Dialogs from "@/pages/Dialogs.vue";
import Auth from "@/pages/Auth.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', component: Dialogs},
        {
            path: '/auth', component: Auth, children: [
                {path: '/auth/login', component: () => import("@/components/LoginForm.vue")},
                {path: '/auth/signup', component: () => import("@/components/RegisterForm.vue")},
            ]
        }
    ],
});

export default router;