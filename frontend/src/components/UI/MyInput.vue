<template>
	<input
		:value="modelValue"
		@input="updateInput"
		type="text"
		class="form-control"
		:placeholder="placeholder"
		:id="id"
	/>
</template>

<script>
export default {
	name: "my-input",
	props: {
		modelValue: [String, Number],
		id: {
			type: String,
			required: true,
		},
		placeholder: {
			type: String,
			default: "Input value",
		},
	},
	setup(props, { emit }) {
		const updateInput = event => {
			let value = event.target.value.trim();
			if (value === "") {
				value = null;
			}
			emit("update:modelValue", value);
		};

		return {
			emit,
		};
	},
	methods: {
		updateInput(event) {
			let value = event.target.value.trim();
			if (value === "") {
				value = null;
			}

			this.$emit("update:modelValue", value);
		},
	},
};
</script>

<style scoped>
.input {
	width: 100%;
	border: 1px solid teal;
	padding: 15px;
	margin-top: 15px;
}
</style>
