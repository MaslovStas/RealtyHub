<template>
	<div v-if="seen" class="d-flex justify-content-center">
		<button
			@click="$emit('loadMore')"
			class="btn btn-danger mt-3"
		>
			Load More
		</button>
	</div>
</template>

<script>
import { computed } from "vue";

export default {
	name: "my-pagination",
	emits: ["loadMore"],
	props: {
		total: {
			type: Number,
			required: true,
		},
		offset: {
			type: Number,
			required: true,
		},
		limit: {
			type: Number,
			required: true,
		},
	},
	setup(props) {
		const seen = computed(() => {
			return props.total - props.offset - props.limit > 0;
		});
		return { seen };
	},
};
</script>
