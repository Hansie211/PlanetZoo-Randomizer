<template>
  <div style="border-radius: 5px; border: 1px solid white; display: flex; flex-direction: row; overflow: hidden; position: relative; align-items: center; width: 100%; height: 250px">
    <img id="thumbnail" :src="animal?.image_url ?? undefined" style="height: 100%; width: 350px; object-fit: contain; background-color: black" />
    <div style="padding: 15px; width: 100%; height: 100%; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center">
      <h3 style="margin: 0; color: #ccc">{{ animal?.title ?? 'No animal selected' }}</h3>
      <h6 style="margin: 0; padding: 0; font-size: 0.8em; color: rgba(255, 255, 255, 0.3)">{{ animal?.edition ?? '' }}</h6>
      <div v-if="!!animal" style="position: absolute; right: 10px; bottom: 10px; display: flex; flex-direction: row; gap: 10px; justify-content: center">
        <span style="font-size: 0.8em">{{ index }} / {{ max }}</span>
        <q-btn icon="arrow_back_ios" size="sm" padding="none" flat @click="(e) => $emit('clickPrevious', e)" />
        <q-btn icon="arrow_forward_ios" size="sm" padding="none" flat @click="(e) => $emit('clickNext', e)" />
        <q-btn icon="casino" size="sm" padding="none" flat @click="(e) => $emit('clickRandomize', e)" />
        <q-btn :href="animal?.wiki_link" padding="none" target="_blank" icon="open_in_new" size="sm" flat />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { AnimalDTO } from 'src/data/animal';
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    animal: {
      type: Object as PropType<AnimalDTO | undefined>,
    },
    index: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
      required: true,
    },
  },
  emits: ['clickRandomize', 'clickNext', 'clickPrevious'],
});
</script>

<style scoped>
@media (max-width: 572px) {
  #thumbnail {
    display: none;
  }
}
</style>
