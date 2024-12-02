<template>
	<div class="container mt-5">
		<div class="card">
			<div class="card-header">
				<h2>{{ realty.title }}</h2>
			</div>
			<div class="card-body">
				<my-carousel :images="realty.images" />
				<hr />
				<p>
					{{ realty.description }}
				</p>
				<hr />
				<p><strong>Price:</strong> ${{ realty.price }}</p>
				<p><strong>Area:</strong> {{ realty.area }} m²</p>
				<p v-if="realty.floor">
					<strong>Floor:</strong>
					{{ realty.floor }}
				</p>
				<p v-if="realty.rooms">
					<strong>Rooms:</strong>
					{{ realty.rooms }}
				</p>
				<p><strong>City:</strong> {{ realty.city }}</p>
				<p><strong>State:</strong> {{ realty.state }}</p>
				<p><strong>Type:</strong> {{ realty.type }}</p>
				<p>
					<strong>Status: </strong>
					<span
						:class="
							realty.is_active
								? 'text-success'
								: 'text-danger'
						"
					>
						<i
							:class="
								realty.is_active
									? 'bi bi-check-circle'
									: 'bi bi-x-circle'
							"
						></i>
						{{ realty.is_active ? "Active" : "Inactive" }}
					</span>
				</p>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		realty: {
			type: Object,
			required: true,
		},
	},
};
</script>
