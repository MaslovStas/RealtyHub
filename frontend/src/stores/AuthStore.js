import { getUserFromJWT } from "@/api/services";
import { defineStore } from "pinia";

export const useAuthStore = defineStore("authStore", {
	state: () => ({
		isLogged: !!localStorage.getItem("accessToken"),
		user: localStorage.getItem("accessToken")
			? getUserFromJWT(localStorage.getItem("accessToken"))
			: null,
	}),
	getters: {
		isOwner: state => user_id => {
			return state.user?.id === user_id;
		},
	},
	actions: {
		login(tokens) {
			localStorage.setItem(
				"accessToken",
				tokens.access_token
			);
			localStorage.setItem(
				"refreshToken",
				tokens.refresh_token
			);
			this.isLogged = true;
		},
		logout() {
			localStorage.removeItem("accessToken");
			localStorage.removeItem("refreshToken");
			this.isLogged = false;
		},
	},
});
