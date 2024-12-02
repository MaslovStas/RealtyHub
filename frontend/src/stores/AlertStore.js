import { defineStore } from "pinia";

export const useAlertStore = defineStore("alertStore", {
	state: () => ({
		message: "",
		alertType: "alert-danger",
		isVisible: false,
	}),
	actions: {
		showAlert(message, type) {
			this.message = message;
			this.alertType = `alert-${type}`;
			this.isVisible = true;

			setTimeout(() => {
				this.isVisible = false;
			}, 3000);
		},
		showError(message) {
			this.showAlert(message, "danger");
		},
		showSuccess(message) {
			this.showAlert(message, "success");
		},
		hideAlert() {
			this.isVisible = false;
		},
	},
});
