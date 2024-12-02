<template>
	<div class="p-3">
		<main>
			<realty-list
				:realtys="realtys"
				:totalRealtys="totalRealtys"
			/>
		</main>
	</div>
</template>

<script>
import { ref, onMounted } from "vue";
import RealtyList from "@/components/RealtyList";
import { useAlertStore } from "@/stores/AlertStore";
import { getMyRealtysApi } from "@/api/requests";

export default {
	components: {
		RealtyList,
	},
	setup() {
		const alertStore = useAlertStore();
		const realtys = ref([]);
		const totalRealtys = ref(0);

		const fetchRealtys = async () => {
			try {
				realtys.value = await getMyRealtysApi();
				totalRealtys.value = realtys.value.length;
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		onMounted(fetchRealtys);

		return { realtys, totalRealtys, fetchRealtys };
	},
};
</script>
