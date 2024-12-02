<template>
	<ul class="nav nav-pills nav-fill">
		<!-- Edit -->
		<li class="nav-item border">
			<router-link
				class="btn"
				:to="{
					name: 'RealtyEdit',
					params: { realty_id: realty.id },
				}"
			>
				<i class="bi bi-pencil text-info"></i> Edit
			</router-link>
		</li>
		<!-- Pause -->
		<li class="nav-item border">
			<button
				type="button"
				class="btn"
				@click="$emit('pause')"
			>
				<i :class="pauseIcon"></i> {{ pauseTitle }}
			</button>
		</li>
		<!-- Delete -->
		<li class="nav-item border">
			<button
				type="button"
				class="btn"
				@click="$emit('remove')"
			>
				<i class="bi bi-trash text-danger"></i> Delete
			</button>
		</li>
	</ul>
</template>

<script>
import { computed } from "vue";
export default {
	emits: ["pause", "remove"],
	props: {
		realty: {
			type: Object,
			required: true,
		},
	},
	setup(props) {
		const pauseTitle = computed(() => {
			return props.realty.is_active
				? "Deactivate"
				: "Activate";
		});
		const pauseIcon = computed(() => {
			return props.realty.is_active
				? "bi bi-pause-circle text-warning"
				: "bi bi-play-circle text-success";
		});
		return { pauseTitle, pauseIcon };
	},
};
</script>
