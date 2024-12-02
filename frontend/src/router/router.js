import LoginPage from "@/pages/LoginPage";
import RegistrationPage from "@/pages/RegistrationPage";
import MainPage from "@/pages/MainPage";
import FavoritesPage from "@/pages/FavoritesPage";
import ProfilePage from "@/pages/ProfilePage";
import MyRealtysPage from "@/pages/MyRealtysPage";
import RealtyPage from "@/pages/RealtyPage";
import RealtyEditPage from "@/pages/RealtyEditPage";
import AddRealtyPage from "@/pages/AddRealtyPage";

import { useAuthStore } from "@/stores/AuthStore";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: "/",
		name: "Main",
		component: MainPage,
	},
	{
		path: "/login",
		name: "Login",
		component: LoginPage,
	},
	{
		path: "/register",
		name: "Registration",
		component: RegistrationPage,
	},
	{
		path: "/favorites",
		name: "Favorites",
		component: FavoritesPage,
		meta: { requiresAuth: true },
	},
	{
		path: "/profile",
		name: "Profile",
		component: ProfilePage,
		meta: { requiresAuth: true },
	},
	{
		path: "/my-realtys",
		name: "MyRealtys",
		component: MyRealtysPage,
		meta: { requiresAuth: true },
	},
	{
		path: "/realtys/:realty_id/edit",
		name: "RealtyEdit",
		component: RealtyEditPage,
		props: true,
	},
	{
		path: "/realtys/:realty_id",
		name: "RealtyDetails",
		component: RealtyPage,
		props: true,
	},
	{
		path: "/new-realty",
		name: "AddRealty",
		component: AddRealtyPage,
		meta: { requiresAuth: true },
	},
];

const router = createRouter({
	routes,
	history: createWebHistory(),
});

router.beforeEach((to, from, next) => {
	const authStore = useAuthStore();

	if (to.meta.requiresAuth && !authStore.isLogged) {
		next({
			name: "Login",
			query: { redirect: to.fullPath },
		});
	} else if (
		["Login", "Registration"].includes(to.name) &&
		authStore.isLogged
	) {
		next({ name: "Main" });
	} else {
		next();
	}
});

export default router;
