<template>
	<div class="row mt-5">
		<form
			class="p-5 col-lg-3 col-md-5 mx-auto border border-2 border-danger rounded-4"
			@submit.prevent
		>
			<h2 class="text-center">Sign Up</h2>
			<!-- Name -->
			<div class="mb-3">
				<label for="inputName" class="form-label"
					>Name</label
				>
				<input
					v-model="form.username"
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
					v-model="form.email"
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
					v-model="form.phone"
					type="tel"
					class="form-control"
					id="inputPhone"
					required
				/>
			</div>
			<!-- Password 1 -->
			<div class="mb-3">
				<label for="inputPassword1" class="form-label"
					>Password</label
				>
				<input
					v-model="form.password1"
					type="password"
					class="form-control"
					id="inputPassword1"
					required
				/>
			</div>
			<!-- Password 2 -->
			<div class="mb-3">
				<label for="inputPassword2" class="form-label"
					>Repeat Password</label
				>
				<input
					v-model="form.password2"
					type="password"
					class="form-control"
					id="inputPassword2"
					required
				/>
			</div>
			<div>
				<router-link
					class="btn btn-link"
					:to="{ name: 'Login' }"
					>Already registered?</router-link
				>
			</div>
			<div class="d-flex justify-content-center">
				<button
					class="btn btn-outline-danger mt-3"
					type="submit"
					@click="register"
					:disabled="!isFormValid"
				>
					Register
				</button>
			</div>
		</form>
	</div>
</template>

<script>
import { reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { getTokenByRegisterApi } from "@/api/requests";
import { useAuthStore } from "@/stores/AuthStore";
import { useAlertStore } from "@/stores/AlertStore";

export default {
	setup() {
		const authStore = useAuthStore();
		const alertStore = useAlertStore();
		const router = useRouter();

		const form = reactive({
			username: "",
			email: "",
			phone: "",
			password1: "",
			password2: "",
		});

		const isFormValid = computed(() => {
			return (
				form.username &&
				form.email &&
				form.phone &&
				form.password1 &&
				form.password1 === form.password2
			);
		});

		const register = async () => {
			try {
				const tokens = await getTokenByRegisterApi(
					form.username,
					form.email,
					form.phone,
					form.password1
				);

				authStore.login(tokens);
				const redirect = router.currentRoute.value.query
					.redirect || {
					name: "Main",
				};
				router.push(redirect);
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		return {
			form,
			isFormValid,
			register,
		};
	},
};
</script>
