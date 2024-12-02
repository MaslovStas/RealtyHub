<template>
	<div class="col">
		<div class="card border-danger h-100">
			<router-link
				:to="{
					name: 'RealtyDetails',
					params: { realty_id: realty.id },
				}"
			>
				<img
					:src="
						realty.title_image
							? realty.title_image.url
							: placeHolderImage
					"
					style="width: 100%; height: 300px"
					class="card-img-top"
					alt="..."
				/>
			</router-link>
			<div class="card-body">
				<h3 class="card-title">
					{{ realty.title }}
				</h3>
				<p class="card-title text-end">
					<strong>{{ realty.price }} ₴</strong>
				</p>
			</div>
			<div
				class="card-footer d-flex justify-content-between"
			>
				<!-- Info -->
				<div class="d-flex align-items-center">
					<div>
						<i class="bi bi-rulers"></i>
						<small class="m-1">{{ realty.area }} м²</small>
					</div>
					<div v-if="realty.rooms">
						<i class="bi bi-houses-fill"></i
						><small class="m-1"
							>{{ realty.rooms }} ком.</small
						>
					</div>
					<div v-if="realty.floor">
						<i class="bi bi-bar-chart-steps"></i
						><small class="m-1"
							>{{ realty.floor }} этаж</small
						>
					</div>
				</div>
				<!-- Favorite -->
				<div v-if="realty.is_favorite != null">
					<button
						class="btn"
						@click="$emit('toggleFavorite', realty)"
					>
						<i
							:class="[
								'text-danger',
								'bi',
								realty.is_favorite
									? 'bi-heart-fill'
									: 'bi-heart',
							]"
						></i>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import placeHolderImage from "@/assets/images/House.png";

export default {
	emits: ["toggleFavorite"],
	props: {
		realty: {
			type: Object,
			required: true,
		},
	},
	setup() {
		return {
			placeHolderImage,
		};
	},
};
</script>
