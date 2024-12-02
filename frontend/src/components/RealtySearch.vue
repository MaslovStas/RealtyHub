<template>
	<!-- Type Realty -->
	<div>
		<label for="selectTypeRealty" class="form-label"
			>Type realty</label
		>
		<my-select
			v-model="selectedSearch.type"
			:options="typeRealtyOptions"
			id="selectTypeRealty"
		/>
	</div>
	<!-- Price -->
	<div class="mt-2">
		<div class="d-flex justify-content-between">
			<!-- Min Price -->
			<div class="flex-grow-1">
				<label for="selectMinPrice" class="form-label"
					>Min Price</label
				>
				<my-input
					id="selectMinPrice"
					v-model="selectedSearch.min_price"
					placeholder="Min:"
				/>
			</div>
			<!-- Max Price -->
			<div class="flex-grow-1">
				<label for="selectMaxPrice" class="form-label"
					>Max Price</label
				>
				<my-input
					id="selectMaxPrice"
					v-model="selectedSearch.max_price"
					placeholder="Max:"
					class="ms-2"
				/>
			</div>
		</div>
	</div>
	<!-- City -->
	<div class="mt-2">
		<label for="selectCity" class="form-label">City</label>
		<my-input
			id="selectCity"
			v-model="selectedSearch.city"
			placeholder="City:"
		/>
	</div>
	<!-- Rooms -->
	<div class="mt-2" v-show="isApartment">
		<label for="selectRooms">Number of rooms</label>
		<my-select
			v-model="selectedSearch.rooms"
			:options="roomsOptions"
			id="selectRooms"
		/>
	</div>
	<!-- With Photos -->
	<div class="mt-3">
		<input
			class="form-check-input"
			type="checkbox"
			id="selectWithPhotos"
			v-model="selectedSearch.with_photos"
		/>
		<label
			class="form-check-label ms-1"
			for="selectWithPhotos"
		>
			With photos
		</label>
	</div>
	<!-- Sort By -->
	<div class="mt-2">
		<label for="">Sort by:</label>
		<my-select
			v-model="selectedSortIndex"
			:options="sortOptions"
			id="selectedSort"
		/>
	</div>
	<!-- Button Reset -->
	<div class="d-flex justify-content-end">
		<button class="btn btn-link mt-3" @click="resetFilter">
			Reset Filter
		</button>
	</div>
	<!-- Button Search -->
	<div class="d-flex justify-content-center">
		<button
			class="btn btn-secondary mt-3"
			@click="searchByFilter"
		>
			<i class="bi bi-search"></i> Search
		</button>
	</div>
	<hr />
</template>

<script>
import { ref, reactive, computed } from "vue";
export default {
	emits: ["search"],
	setup(props, { emit }) {
		const typeRealtyOptions = [
			{ value: "", name: "All Realty" },
			{ value: "APARTMENT", name: "Apartment" },
			{ value: "HOUSE", name: "House" },
			{ value: "COMMERCIAL", name: "Commercial" },
		];
		const roomsOptions = [
			{ value: "", name: "All Realty" },
			{ value: "1", name: "1 rooms" },
			{ value: "2", name: "2 rooms" },
			{ value: "3", name: "3 rooms" },
			{ value: "4", name: "4 rooms" },
			{ value: "5", name: "5+ rooms" },
		];
		const sortOptions = [
			{
				value: "0",
				name: "The newest",
			},
			{
				value: "1",
				name: "The oldest",
			},
			{
				value: "2",
				name: "The cheapest",
			},
			{
				value: "3",
				name: "The most expensive",
			},
		];
		const sortList = [
			{
				order_by: "created_at",
				desc_order: true,
			},
			{
				order_by: "created_at",
				desc_order: false,
			},
			{
				order_by: "price",
				desc_order: false,
			},
			{
				order_by: "price",
				desc_order: true,
			},
		];
		const selectedSortIndex = ref("0");
		const selectedSearch = reactive({});

		const selectedSort = computed(() => {
			return sortList[selectedSortIndex.value];
		});
		const isApartment = computed(() => {
			return selectedSearch.type === "APARTMENT";
		});
		const roomsApartment = computed(() => {
			return isApartment.value
				? selectedSearch.rooms
				: null;
		});

		const resetFilter = () => {
			Object.assign(selectedSearch, {
				type: null,
				min_price: null,
				max_price: null,
				rooms: null,
				with_photos: false,
				city: null,
				limit: 20,
			});
			selectedSortIndex.value = "0";
		};
		const searchByFilter = () => {
			selectedSearch.rooms = roomsApartment.value;
			emit("search", {
				...selectedSearch,
				...selectedSort.value,
			});
		};

		resetFilter();

		return {
			typeRealtyOptions,
			roomsOptions,
			sortOptions,
			selectedSortIndex,
			selectedSearch,
			selectedSort,
			isApartment,
			resetFilter,
			searchByFilter,
		};
	},
};
</script>
