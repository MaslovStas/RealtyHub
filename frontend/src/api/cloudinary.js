import axios from "axios";

const CLOUD_NAME = "dthagcqvj";
const CLOUDINARY_URL = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`;

const CLOUDINARY_UPLOAD_PRESET = "realtys";

const uploadImageApi = async imageURL => {
	const formData = new FormData();
	formData.append("file", imageURL);
	formData.append(
		"upload_preset",
		CLOUDINARY_UPLOAD_PRESET
	);

	const response = await axios.post(
		CLOUDINARY_URL,
		formData
	);
	const data = response.data;

	return data;
};

export { uploadImageApi };
