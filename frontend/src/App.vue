<template>
	<div class="p-3">
		<!-- NavBar -->
		<nav-bar />
		<!-- Alert -->
		<div
			v-if="alertStore.isVisible"
			:class="[
				'alert',
				alertStore.alertType,
				'alert-dismissible',
				'fade',
				'show',
			]"
			role="alert"
		>
			{{ alertStore.message }}
			<button
				type="button"
				class="btn-close"
				@click="alertStore.hideAlert"
				aria-label="Close"
			></button>
		</div>
		<!-- Content -->
		<router-view />
		<!-- <router-view v-slot="{ Component }">
			<keep-alive>
				<component :is="Component" />
			</keep-alive>
		</router-view> -->
	</div>
</template>

<script>
import { useAlertStore } from "@/stores/AlertStore";
import NavBar from "@/components/NavBar";

export default {
	components: {
		NavBar,
	},
	setup() {
		const alertStore = useAlertStore();
		return { alertStore };
	},
};
</script>
