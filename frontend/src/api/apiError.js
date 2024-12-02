class ApiError extends Error {
	constructor(message, statusCode) {
		super(message);
		this.statusCode = statusCode;
	}
}

class NotAuthenticated extends ApiError {
	constructor(message = "Not Authenticated") {
		super(message, 401);
	}
}

class NotFound extends ApiError {
	constructor(message = "Not Found") {
		super(message, 404);
	}
}

const handleApiError = error => {
	if (error.response) {
		const message = error.response.data.detail;
		const status = error.response.status;

		switch (status) {
			case 401:
				return new NotAuthenticated(message);
			case 404:
				return new NotFound(message);
			default:
				return new ApiError(message, status);
		}
	} else if (error.request) {
		return new ApiError("Error connection", null);
	} else {
		return new ApiError(
			`Error request: ${error.message}`,
			null
		);
	}
};

export {
	ApiError,
	NotAuthenticated,
	NotFound,
	handleApiError,
};
