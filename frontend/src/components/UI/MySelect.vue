<template>
	<select
		class="form-select text-secondary"
		:value="modelValue"
		@change="changeOption"
		:id="id"
	>
		<option
			v-for="option in options"
			:key="option.value"
			:value="option.value"
		>
			{{ option.name }}
		</option>
	</select>
</template>

<script>
export default {
	name: "my-select",
	props: {
		modelValue: {
			type: [String],
		},
		id: {
			type: String,
			required: true,
		},
		options: {
			type: Array,
			default: () => [],
		},
	},
	setup(props, { emit }) {
		const changeOption = event => {
			let newValue = event.target.value;

			if (newValue === "") {
				newValue = null;
			}
			emit("update:modelValue", newValue);
		};
		return { changeOption };
	},
};
</script>
