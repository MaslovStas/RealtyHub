<template>
	<form @submit.prevent>
		<!-- Images -->
		<div class="row">
			<div
				class="col-md-4 col-sm-6 d-flex flex-column align-items-center justify-content-between"
				v-for="(image, index) in localRealty.images"
				:key="index"
			>
				<img
					:src="image.url"
					class="rounded mx-auto d-block mt-3"
					alt="..."
					style="width: 200px; height: 200px"
				/>
				<ul class="nav nav-pills nav-fill mt-3">
					<!-- Up -->
					<li class="nav-item border">
						<button
							type="button"
							class="btn"
							@click="up(index)"
						>
							<i class="bi bi-arrow-up text-info"></i>
						</button>
					</li>
					<!-- Down -->
					<li class="nav-item border">
						<button
							type="button"
							class="btn"
							@click="down(index)"
						>
							<i class="bi bi-arrow-down text-info"></i>
						</button>
					</li>
					<!-- Delete -->
					<li class="nav-item border">
						<button
							type="button"
							class="btn"
							@click="remove(index)"
						>
							<i class="bi bi-x text-danger"></i>
						</button>
					</li>
				</ul>
			</div>
		</div>
		<!-- Upload Image -->
		<div class="mt-3">
			<label for="formFile" class="form-label"
				>Photos</label
			>
			<input
				class="form-control"
				type="file"
				id="formFile"
				@change="upload"
				accept="image/*"
			/>
		</div>

		<!-- Type -->
		<div class="mt-3">
			<label for="selectTypeRealty" class="form-label"
				>Type realty</label
			>
			<my-select
				v-model="localRealty.type"
				:options="typeRealtyOptions"
				id="selectTypeRealty"
			/>
		</div>
		<!-- Title -->
		<div class="mt-3">
			<label for="inputTitle" class="form-label"
				>Title
			</label>
			<input
				type="text"
				class="form-control"
				id="inputTitle"
				v-model="localRealty.title"
				required
			/>
		</div>
		<!-- Description -->
		<div class="mt-3">
			<label for="inputDescription" class="form-label"
				>Description
			</label>
			<textarea
				class="form-control"
				id="inputDescription"
				rows="3"
				v-model="localRealty.description"
				required
			></textarea>
		</div>
		<!-- Price -->
		<div class="mt-3">
			<label for="inputPrice" class="form-label"
				>Price, $</label
			>
			<input
				type="number"
				class="form-control"
				id="inputPrice"
				v-model="localRealty.price"
				required
			/>
		</div>
		<!-- Area -->
		<div class="mt-3">
			<label for="inputArea" class="form-label">Area</label>
			<input
				type="number"
				class="form-control"
				id="inputArea"
				v-model="localRealty.area"
				required
			/>
		</div>
		<!-- Floor -->
		<div class="mt-3" v-if="isApartment">
			<label for="inputFloor" class="form-label"
				>Floor</label
			>
			<input
				type="number"
				class="form-control"
				id="inputFloor"
				v-model="localRealty.floor"
				required
			/>
		</div>
		<!-- Rooms -->
		<div class="mt-3" v-if="isApartment">
			<label for="inputRooms" class="form-label"
				>Rooms</label
			>
			<input
				type="number"
				class="form-control"
				id="inputRooms"
				v-model="localRealty.rooms"
				required
			/>
		</div>
		<!-- City -->
		<div class="mt-3">
			<label for="inputCity" class="form-label">City</label>
			<input
				type="text"
				class="form-control"
				id="inputCity"
				v-model="localRealty.city"
				required
			/>
		</div>
		<!-- State -->
		<div class="mt-3">
			<label for="inputState" class="form-label"
				>State</label
			>
			<input
				type="text"
				class="form-control"
				id="inputState"
				v-model="localRealty.state"
				required
			/>
		</div>
		<!-- Save Button -->
		<div class="mt-3 d-flex justify-content-center">
			<button
				class="btn btn-danger"
				type="submit"
				@click="save"
				:disabled="!isFormValid"
			>
				Save
			</button>
		</div>
	</form>
</template>

<script>
import { useAlertStore } from "@/stores/AlertStore";
import { uploadImageApi } from "@/api/cloudinary";
import { reactive, computed } from "vue";

export default {
	emits: ["save"],
	props: {
		realty: {
			type: Object,
			default: () => ({
				type: "",
				title: "",
				description: "",
				price: null,
				area: null,
				floor: null,
				rooms: null,
				city: "",
				state: "",
				is_active: true,
				images: [],
			}),
		},
	},
	setup(props, { emit }) {
		const alertStore = useAlertStore();
		const localRealty = reactive(
			JSON.parse(JSON.stringify(props.realty))
		);
		const typeRealtyOptions = [
			{ value: "", name: "Select Type Realty" },
			{ value: "APARTMENT", name: "Apartment" },
			{ value: "HOUSE", name: "House" },
			{ value: "COMMERCIAL", name: "Commercial" },
		];

		const up = index => {
			if (index > 0) {
				const temp = localRealty.images[index];
				localRealty.images[index] =
					localRealty.images[index - 1];
				localRealty.images[index - 1] = temp;
			}
		};
		const down = index => {
			if (index < localRealty.images.length - 1) {
				const temp = localRealty.images[index];
				localRealty.images[index] =
					localRealty.images[index + 1];
				localRealty.images[index + 1] = temp;
			}
		};
		const remove = index => {
			localRealty.images.splice(index, 1);
		};

		const upload = event => {
			const file = event.target.files[0];
			if (!file) return;

			const reader = new FileReader();
			reader.onload = e => {
				const image = {
					url: e.target.result,
					public_id: null,
				};
				localRealty.images.push(image);
			};
			reader.readAsDataURL(file);
		};
		const save = async () => {
			try {
				const uploadPromises = localRealty.images.map(
					async (image, index) => {
						if (!image.public_id) {
							const data = await uploadImageApi(image.url);
							localRealty.images[index] = {
								url: data.url,
								public_id: data.public_id,
							};
						}
					}
				);

				await Promise.all(uploadPromises);

				emit("save", localRealty);
			} catch (error) {
				alertStore.showError(error);
			}
		};

		const isApartment = computed(() => {
			return localRealty.type === "APARTMENT";
		});
		const isFormValid = computed(() => {
			const requiredFields = [
				localRealty.type,
				localRealty.title,
				localRealty.description,
				localRealty.price,
				localRealty.area,
				localRealty.city,
				localRealty.state,
			];
			const positiveFields = [
				localRealty.price > 0,
				localRealty.area > 0,
			];
			const apartmentFields =
				!isApartment.value ||
				(localRealty.floor > 0 && localRealty.rooms > 0);

			return (
				requiredFields.every(field => !!field) &&
				positiveFields.every(field => field) &&
				apartmentFields
			);
		});

		return {
			localRealty,
			typeRealtyOptions,
			up,
			down,
			remove,
			upload,
			save,
			isApartment,
			isFormValid,
		};
	},
};
</script>
