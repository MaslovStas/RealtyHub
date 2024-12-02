<template>
	<div class="p-3">
		<main>
			<realty-list
				:realtys="realtys"
				:totalRealtys="totalRealtys"
				@toggleFavorite="toggleFavorite"
			/>
		</main>
	</div>
</template>

<script>
import { ref, onMounted } from "vue";
import RealtyList from "@/components/RealtyList";
import { useAlertStore } from "@/stores/AlertStore";
import {
	removeFavoriteApi,
	getFavoritesRealtysApi,
} from "@/api/requests";

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
				const [loadedRealtys, totalRealtysCount] =
					await getFavoritesRealtysApi();
				loadedRealtys.forEach(realty => {
					realty.is_favorite = true;
				});
				realtys.value = loadedRealtys;
				totalRealtys.value = +totalRealtysCount;
			} catch (error) {
				alertStore.showError(error.message);
			}
		};
		const toggleFavorite = async realty => {
			try {
				await removeFavoriteApi(realty.id);
				realtys.value = realtys.value.filter(
					r => r.id !== realty.id
				);
				totalRealtys.value -= 1;
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		onMounted(fetchRealtys);

		return { realtys, totalRealtys, toggleFavorite };
	},
};
</script>
