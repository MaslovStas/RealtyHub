<template>
	<div class="row mt-5">
		<form
			class="p-5 col-lg-3 col-md-5 mx-auto border border-2 border-danger rounded-4"
			@submit.prevent
		>
			<h2 class="text-center">Profile</h2>
			<!-- Name -->
			<div class="mb-3">
				<label for="inputName" class="form-label"
					>Name</label
				>
				<input
					v-model="user.username"
					type="text"
					class="form-control"
					id="inputName"
					required
				/>
			</div>
			<!-- Email -->
			<div class="mb-3">
				<label for="InputEmail" class="form-label"
					>Email</label
				>
				<input
					v-model="user.email"
					type="email"
					class="form-control"
					id="inputEmail"
					required
				/>
			</div>
			<!-- Phone -->
			<div class="mb-3">
				<label for="InputPhone" class="form-label"
					>Phone</label
				>
				<input
					v-model="user.phone"
					type="tel"
					class="form-control"
					id="inputPhone"
					required
				/>
			</div>
			<div class="d-flex justify-content-center">
				<button
					class="btn btn-outline-danger mt-3"
					type="submit"
					@click="updateProfile"
					:disabled="!isFormValid"
				>
					Save
				</button>
			</div>
		</form>
	</div>
</template>

<script>
import { reactive, computed, onMounted } from "vue";
import { useAlertStore } from "@/stores/AlertStore";
import {
	getUserProfileApi,
	updateUserProfileApi,
} from "@/api/requests";

export default {
	setup() {
		const alertStore = useAlertStore();
		const user = reactive({
			id: 0,
			username: "",
			email: "",
			phone: "",
		});

		const isFormValid = computed(() => {
			return user.username && user.email && user.phone;
		});

		const getProfile = async () => {
			try {
				Object.assign(user, await getUserProfileApi());
			} catch (error) {
				alertStore.showError(error.message);
			}
		};
		const updateProfile = async () => {
			try {
				await updateUserProfileApi(user);
				alertStore.showSuccess("Profile updated!");
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		onMounted(getProfile);

		return { user, getProfile, updateProfile, isFormValid };
	},
};
</script>
