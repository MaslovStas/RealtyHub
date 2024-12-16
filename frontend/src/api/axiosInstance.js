import axios from "axios";
import { useAuthStore } from "@/stores/AuthStore";

import {
	handleApiError,
	NotAuthenticated,
} from "@/api/apiError";

const baseURL =
	process.env.VUE_APP_API_BASE_URL || "http://backend:8000";

const addAutorizationHeader = config => {
	const accessToken = localStorage.getItem("accessToken");

	if (accessToken) {
		config.headers[
			"Authorization"
		] = `Bearer ${accessToken}`;
	} else {
		delete config.headers["Authorization"];
	}
};

const updateTokens = async () => {
	const refreshToken = localStorage.getItem("refreshToken");

	if (refreshToken) {
		const authStore = useAuthStore();

		try {
			const response = await axios.post(
				`${baseURL}/auth/jwt/refresh`,
				{},
				{
					headers: {
						Authorization: `Bearer ${refreshToken}`,
						"Content-Type":
							"application/x-www-form-urlencoded",
						Accept: "application/json",
					},
				}
			);
			const tokens = response.data;

			authStore.login(tokens);
		} catch (error) {
			if (error instanceof NotAuthenticated) {
				authStore.logout();
			}
			throw error;
		}
	}
};

const axiosInstance = axios.create({
	baseURL: baseURL,
	headers: {
		"Content-Type": "application/json",
		Accept: "application/json",
	},
});

axiosInstance.interceptors.request.use(
	config => {
		addAutorizationHeader(config);

		return config;
	},
	error => {
		return Promise.reject(error);
	}
);

axiosInstance.interceptors.response.use(
	response => {
		return response;
	},
	async error => {
		const originalRequest = error.config;
		const authStore = useAuthStore();
		const ApiError = handleApiError(error);

		if (
			ApiError instanceof NotAuthenticated &&
			authStore.isLogged &&
			!originalRequest._retry
		) {
			originalRequest._retry = true;
			try {
				await updateTokens();
				return axiosInstance(originalRequest);
			} catch (refreshError) {}
			return Promise.reject(refreshError);
		}

		return Promise.reject(ApiError);
	}
);

export default axiosInstance;
