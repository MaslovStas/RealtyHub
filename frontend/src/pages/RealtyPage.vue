<template>
	<realty-actions
		v-if="isOwnerRealty"
		:realty="realty"
		@remove="removeRealty"
		@pause="pauseRealty"
	/>
	<realty-details :realty="realty" />
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
	getRealtyApi,
	updateRealtyApi,
	removeRealtyApi,
} from "@/api/requests";
import RealtyDetails from "@/components/RealtyDetails";
import RealtyActions from "@/components/RealtyActions";
import { useAuthStore } from "@/stores/AuthStore";
import { useAlertStore } from "@/stores/AlertStore";

export default {
	components: {
		RealtyDetails,
		RealtyActions,
	},
	props: {
		realty_id: {
			type: String,
			required: true,
		},
	},
	setup(props) {
		const authStore = useAuthStore();
		const alertStore = useAlertStore();
		const router = useRouter();

		const realty = ref({});

		const isOwnerRealty = computed(() => {
			return authStore.isOwner(realty.value.user_id);
		});

		const fetchRealty = async () => {
			try {
				realty.value = await getRealtyApi(props.realty_id);
			} catch (error) {
				alertStore.showError(error.message);
			}
		};
		const pauseRealty = async () => {
			try {
				const data = {
					is_active: !realty.value.is_active,
					type: realty.value.type,
				};

				realty.value = await updateRealtyApi(
					realty.value.id,
					data
				);
			} catch (error) {
				alertStore.showError(error.message);
			}
		};
		const removeRealty = async () => {
			try {
				await removeRealtyApi(realty.value.id);
				alertStore.showSuccess("Realty removed");
				router.push({ name: "Main" });
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		onMounted(fetchRealty);

		return {
			authStore,
			alertStore,
			realty,
			isOwnerRealty,
			fetchRealty,
			pauseRealty,
			removeRealty,
		};
	},
};
</script>
