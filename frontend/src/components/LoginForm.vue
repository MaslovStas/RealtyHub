<template>
	<div class="row mt-5">
		<form
			class="p-5 col-lg-3 col-md-5 mx-auto border border-2 border-danger rounded-4"
			@submit.prevent
		>
			<h2 class="text-center">Sign In</h2>
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
			<!-- Password -->
			<div class="mb-3">
				<label for="inputPassword" class="form-label"
					>Password</label
				>
				<input
					v-model="form.password"
					type="password"
					class="form-control"
					id="inputPassword"
					required
				/>
			</div>
			<!-- Register -->
			<div>
				<router-link
					class="btn btn-link"
					:to="{ name: 'Registration' }"
					>Not registered yet?</router-link
				>
			</div>
			<!-- Enter -->
			<div class="d-flex justify-content-center">
				<button
					class="btn btn-outline-danger mt-3"
					type="submit"
					@click="login"
					:disabled="!isFormValid"
				>
					Enter
				</button>
			</div>
		</form>
	</div>
</template>

<script>
import { reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { getTokenByLoginApi } from "@/api/requests";
import { useAuthStore } from "@/stores/AuthStore";
import { useAlertStore } from "@/stores/AlertStore";

export default {
	setup() {
		const authStore = useAuthStore();
		const alertStore = useAlertStore();
		const router = useRouter();

		const form = reactive({
			email: "",
			password: "",
		});

		const isFormValid = computed(() => {
			return form.email && form.password;
		});

		const login = async () => {
			try {
				const tokens = await getTokenByLoginApi(
					form.email,
					form.password
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
			login,
		};
	},
};
</script>
