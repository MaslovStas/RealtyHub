<template>
	<nav
		class="navbar navbar-expand-lg navbar-light bg-light"
	>
		<div class="container-fluid">
			<!-- Logo -->
			<router-link
				class="navbar-brand"
				:to="{ name: 'Main' }"
			>
				<img
					src="@/assets/images/logo.png"
					alt="RealtyHub"
					width="64"
					height="64"
				/>
			</router-link>
			<button
				class="navbar-toggler"
				type="button"
				data-bs-toggle="collapse"
				data-bs-target="#navbarSupportedContent"
				aria-controls="navbarSupportedContent"
				aria-expanded="false"
				aria-label="Переключатель навигации"
			>
				<span class="navbar-toggler-icon"></span>
			</button>
			<div
				class="collapse navbar-collapse"
				id="navbarSupportedContent"
			>
				<ul class="navbar-nav d-flex ms-auto">
					<div v-if="isLogged" class="d-lg-flex">
						<!-- Favorites -->
						<li class="nav-item">
							<router-link
								active-class="active"
								class="btn"
								:to="{ name: 'Favorites' }"
							>
								Favorites
							</router-link>
						</li>
						<!-- Add Realty -->
						<li class="nav-item">
							<router-link
								active-class="active"
								class="btn"
								:to="{ name: 'AddRealty' }"
							>
								Add Realty
							</router-link>
						</li>
						<!-- My Realtys -->
						<li class="nav-item">
							<router-link
								active-class="active"
								class="btn"
								:to="{ name: 'MyRealtys' }"
							>
								My Realtys
							</router-link>
						</li>
						<!-- Profile -->
						<li class="nav-item">
							<router-link
								active-class="active"
								class="btn"
								:to="{ name: 'Profile' }"
							>
								Profile
							</router-link>
						</li>
						<!-- Logout -->
						<li class="nav-item">
							<button
								type="button"
								class="btn"
								@click="logout"
							>
								Logout
							</button>
						</li>
					</div>
					<!-- Login -->
					<div v-else>
						<li class="nav-item">
							<router-link
								active-class="active"
								class="btn"
								:to="{ name: 'Login' }"
							>
								Login
							</router-link>
						</li>
					</div>
				</ul>
			</div>
		</div>
	</nav>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/AuthStore";

export default {
	setup() {
		const authStore = useAuthStore();
		const router = useRouter();

		const isLogged = computed(() => {
			return authStore.isLogged;
		});

		const logout = () => {
			authStore.logout();
			if (router.currentRoute.value.path === "/") {
				window.location.reload();
			} else {
				router.push("/");
			}
		};

		return { isLogged, logout };
	},
};
</script>
