function decodeJWT(token) {
	const base64Url = token.split(".")[1];
	const base64 = base64Url
		.replace(/-/g, "+")
		.replace(/_/g, "/");
	const jsonPayload = decodeURIComponent(
		atob(base64)
			.split("")
			.map(
				c =>
					"%" +
					("00" + c.charCodeAt(0).toString(16)).slice(-2)
			)
			.join("")
	);

	return JSON.parse(jsonPayload);
}

const getUserFromJWT = token => {
	try {
		const payload = decodeJWT(token);
		return {
			id: payload.sub,
			username: payload.username,
		};
	} catch (error) {
		return null;
	}
};

export { decodeJWT, getUserFromJWT };
