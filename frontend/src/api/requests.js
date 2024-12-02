import axiosInstance from "@/api/axiosInstance";

const getRealtysApi = async filterQuery => {
	const config = {
		method: "GET",
		url: "/realtys/",
		params: { ...filterQuery },
	};
	const response = await axiosInstance(config);

	const realtys = response.data;
	const totalRealtys = response.headers["x-total-count"];

	return [realtys, totalRealtys];
};

const getRealtyApi = async realty_id => {
	const config = {
		method: "GET",
		url: `/realtys/${realty_id}/`,
	};
	const response = await axiosInstance(config);

	return response.data;
};

const createRealtyApi = async data => {
	const config = {
		method: "POST",
		url: "/realtys/",
		data: data,
	};
	const response = await axiosInstance(config);

	return response.data;
};

const updateRealtyApi = async (realty_id, data) => {
	const config = {
		method: "PATCH",
		url: `/realtys/${realty_id}/`,
		data: data,
	};
	const response = await axiosInstance(config);

	return response.data;
};

const removeRealtyApi = async realty_id => {
	const config = {
		method: "DELETE",
		url: `/realtys/${realty_id}/`,
	};
	await axiosInstance(config);
};

const getFavoritesRealtysApi = async () => {
	const config = {
		method: "GET",
		url: "/realtys/favorites",
	};
	const response = await axiosInstance(config);

	const realtys = response.data;
	const totalRealtys = response.headers["x-total-count"];

	return [realtys, totalRealtys];
};

const addFavoriteApi = async realty_id => {
	const config = {
		method: "POST",
		url: `/realtys/favorites/${realty_id}/`,
	};
	await axiosInstance(config);
};

const removeFavoriteApi = async realty_id => {
	const config = {
		method: "DELETE",
		url: `/realtys/favorites/${realty_id}/`,
	};
	await axiosInstance(config);
};

const getTokenByLoginApi = async (email, password) => {
	const data = new URLSearchParams({
		grant_type: "password",
		username: email,
		password: password,
	});
	const config = {
		method: "POST",
		url: "/auth/jwt/token",
		data: data,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
	};
	const response = await axiosInstance(config);

	return response.data;
};

const getTokenByRegisterApi = async (
	username,
	email,
	phone,
	password
) => {
	const data = {
		username: username,
		email: email,
		phone: phone,
		password: password,
	};
	const config = {
		method: "POST",
		url: "/auth/jwt/register",
		data: data,
	};
	const response = await axiosInstance(config);

	return response.data;
};

const getUserProfileApi = async () => {
	const config = {
		method: "GET",
		url: "/users/me/",
	};
	const response = await axiosInstance(config);

	return response.data;
};

const updateUserProfileApi = async user => {
	const config = {
		method: "PATCH",
		url: `/users/${user.id}/`,
		data: user,
	};
	await axiosInstance(config);
};

const getMyRealtysApi = async () => {
	const config = {
		method: "GET",
		url: `/users/me/realtys`,
	};
	const response = await axiosInstance(config);

	return response.data;
};

export {
	getRealtysApi,
	getRealtyApi,
	createRealtyApi,
	updateRealtyApi,
	removeRealtyApi,
	getFavoritesRealtysApi,
	addFavoriteApi,
	removeFavoriteApi,
	getTokenByLoginApi,
	getTokenByRegisterApi,
	getUserProfileApi,
	updateUserProfileApi,
	getMyRealtysApi,
};
