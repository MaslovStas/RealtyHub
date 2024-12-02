<template>
	<div>
		<h4 class="text-center mt-3">Add Realty</h4>
		<realty-form @save="createRealty" />
	</div>
</template>

<script>
import { useRouter } from "vue-router";
import { createRealtyApi } from "@/api/requests";
import { useAlertStore } from "@/stores/AlertStore";
import RealtyForm from "@/components/RealtyForm";
export default {
	components: {
		RealtyForm,
	},
	setup() {
		const router = useRouter();
		const alertStore = useAlertStore();

		const createRealty = async realty => {
			try {
				const newRealty = await createRealtyApi(realty);
				router.push({
					name: "RealtyDetails",
					params: { realty_id: newRealty.id },
				});
			} catch (error) {
				alertStore.showError(error.message);
			}
		};
		return {
			createRealty,
		};
	},
};
</script>
