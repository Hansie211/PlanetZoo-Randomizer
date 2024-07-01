<template>
  <div class="grid-wrapper">
    <h6 class="grid-title">{{ title }}</h6>
    <div class="grid">
      <template v-for="(value, index) in options" :key="value">
        <q-btn :style="{ 'background-color': selectedValues.includes(value) ? 'white' : '#FFFFFF50' }" align="left" text-color="black" @click="() => selectValue(value)"
          ><q-checkbox v-model="selectedValues" :val="value" :label="option_labels[index]" />
        </q-btn>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref, PropType } from 'vue';

const equalArrays = <T>(a: T[], b: T[]) => {
  if (a.length !== b.length) {
    return false;
  }

  for (let i = 0; i < a.length; i++) {
    if (!b.includes(a[i])) {
      return false;
    }
  }

  return true;
};

export default defineComponent({
  props: {
    title: {
      type: String,
      requiered: true,
    },
    options: {
      type: Array as PropType<string[]>,
      required: true,
    },
    labels: {
      type: Array as PropType<string[]>,
    },
  },
  emits: ['onUpdateValues'],

  setup(props) {
    const selectedValues: Ref<string[]> = ref([...props.options]);
    let previousSelectedValues = [...selectedValues.value];

    return {
      selectedValues,
      previousSelectedValues,
      option_labels: props.labels ?? props.options,
    };
  },

  methods: {
    selectValue(value: string) {
      if (this.selectedValues.includes(value)) {
        this.removeValue(value);
      } else {
        this.addValue(value);
      }
    },

    removeValue(value: string) {
      this.selectedValues = this.selectedValues.filter((x) => x !== value);
    },

    addValue(value: string) {
      this.selectedValues.push(value);
    },
  },

  watch: {
    'selectedValues.length': function (nValue) {
      if (nValue === 0) {
        this.selectedValues = [...this.previousSelectedValues];
      } else if (equalArrays(this.previousSelectedValues, this.selectedValues)) {
        // don't emit
      } else {
        this.$emit('onUpdateValues', this.selectedValues);
        this.previousSelectedValues = [...this.selectedValues];
      }
    },
  },
});
</script>

<style scoped>
.grid-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 5px;
}

.grid-title {
  height: 40px;
  flex-grow: 0;
  flex-shrink: 0;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: flex-end;
  color: #ccc;
}

.grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-column-gap: 7px;
  grid-row-gap: 7px;
}
</style>
