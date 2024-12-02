<template>
	<div id="carousel" class="carousel slide">
		<div class="carousel-inner">
			<div
				:class="['carousel-item', { active: index === 0 }]"
				v-for="(image, index) in images"
				:key="image.id"
			>
				<img
					:src="image.url"
					class="d-block w-100"
					:alt="image.public_id"
				/>
			</div>
		</div>
		<button
			class="carousel-control-prev"
			type="button"
			data-bs-target="#carousel"
			data-bs-slide="prev"
		>
			<span
				class="carousel-control-prev-icon"
				aria-hidden="true"
			></span>
			<span class="visually-hidden">Previous</span>
		</button>
		<button
			class="carousel-control-next"
			type="button"
			data-bs-target="#carousel"
			data-bs-slide="next"
		>
			<span
				class="carousel-control-next-icon"
				aria-hidden="true"
			></span>
			<span class="visually-hidden">Next</span>
		</button>
	</div>
</template>

<script>
export default {
	name: "my-carousel",
	props: {
		images: {
			type: Array,
			default: () => [],
		},
	},
};
</script>

