<template>
	<div class="p-3">
		<main>
			<realty-search @search="search" />

			<realty-list
				:realtys="realtys"
				:totalRealtys="totalRealtys"
				@toggleFavorite="toggleFavorite"
			/>
			<my-pagination
				@load-more="loadMore"
				:offset="filterQuery.offset"
				:limit="filterQuery.limit"
				:total="totalRealtys"
			/>
		</main>
	</div>
</template>

<script>
import RealtyList from "@/components/RealtyList";
import RealtySearch from "@/components/RealtySearch";
import { useAlertStore } from "@/stores/AlertStore";
import { ref, reactive } from "vue";

import {
	getRealtysApi,
	addFavoriteApi,
	removeFavoriteApi,
} from "@/api/requests";
import { onMounted } from "vue";
export default {
	components: {
		RealtySearch,
		RealtyList,
	},
	setup() {
		const alertStore = useAlertStore();
		const realtys = ref([]);
		const totalRealtys = ref(0);
		const filterQuery = reactive({
			offset: 0,
			limit: 20,
			type: null,
			min_price: null,
			max_price: null,
			rooms: null,
			city: null,
			with_photos: null,
			order_by: null,
			desc_order: null,
		});

		const fetchRealtys = async () => {
			try {
				const [loadedRealtys, totalRealtysCount] =
					await getRealtysApi(filterQuery);

				realtys.value.push(...loadedRealtys);
				totalRealtys.value = parseInt(totalRealtysCount);
			} catch (error) {
				alertStore.showError(error.message);
			}
		};
		const search = async userFilterQuery => {
			Object.assign(filterQuery, userFilterQuery);
			filterQuery.offset = 0;
			realtys.value = [];
			await fetchRealtys();
		};
		const loadMore = async () => {
			const currentOffset = filterQuery.offset;
			filterQuery.offset += filterQuery.limit;
			try {
				await fetchRealtys();
			} catch (error) {
				filterQuery.offset = currentOffset;
			}
		};
		const toggleFavorite = async realty => {
			try {
				realty.is_favorite
					? await removeFavoriteApi(realty.id)
					: await addFavoriteApi(realty.id);
				realty.is_favorite = !realty.is_favorite;
			} catch (error) {
				alertStore.showError(error.message);
			}
		};

		onMounted(fetchRealtys);

		return {
			realtys,
			totalRealtys,
			filterQuery,
			search,
			loadMore,
			toggleFavorite,
		};
	},
};
</script>
