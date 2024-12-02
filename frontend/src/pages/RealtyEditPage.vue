<template>
	<h1>Edit Realty</h1>
	<realty-form
		v-if="realty"
		@save="updateRealty"
		:realty="realty"
	/>
</template>

<script>
import {
	getRealtyApi,
	updateRealtyApi,
} from "@/api/requests";
import { useAlertStore } from "@/stores/AlertStore";
import RealtyForm from "@/components/RealtyForm";
import { ref, onMounted } from "vue";

export default {
	components: {
		RealtyForm,
	},
	props: {
		realty_id: {
			type: String,
			required: true,
		},
	},
	setup(props) {
		const realty = ref(null);
		const alertStore = useAlertStore();

		const fetchRealty = async () => {
			try {
				realty.value = await getRealtyApi(props.realty_id);
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		const updateRealty = async realtyForm => {
			try {
				await updateRealtyApi(realtyForm.id, realtyForm);
				alertStore.showSuccess("Realty updated!");
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		onMounted(fetchRealty);

		return {
			realty,
			updateRealty,
		};
	},
};
</script>
