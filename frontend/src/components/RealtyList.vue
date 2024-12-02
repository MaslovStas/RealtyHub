<template>
	<h4>Total {{ totalRealtys }} Realtys</h4>

	<div class="row row-cols-1 row-cols-md-3 g-2 mt-3">
		<transition-group name="realty-list">
			<realty-item
				v-for="realty in realtys"
				:realty="realty"
				:key="realty.id"
				@toggleFavorite="$emit('toggleFavorite', realty)"
			/>
		</transition-group>
	</div>
</template>

<script>
import RealtyItem from "@/components/RealtyItem";

export default {
	components: {
		RealtyItem,
	},
	emits: ["toggleFavorite"],
	props: {
		realtys: {
			type: Array,
			required: true,
		},
		totalRealtys: {
			type: Number,
			required: true,
		},
	},
};
</script>

<style scoped>
.realty-list-item {
	display: inline-block;
	margin-right: 10px;
}
.realty-list-enter-active,
.realty-list-leave-active {
	transition: all 0.6s ease;
}
.realty-list-enter-from,
.realty-list-leave-to {
	opacity: 0;
	transform: translateY(30px);
}
</style>
