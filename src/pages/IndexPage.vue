<template>
  <q-page class="row items-center justify-evenly">
    <div style="background-color: #555; padding: 10px; border-radius: 5px">
      <animal-selector />
    </div>

    <img src="~/assets/screenshot_1.jpg" style="position: absolute; z-index: -1; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; filter: blur(2px)" />
  </q-page>
</template>

<script lang="ts">
import AnimalSelector from 'src/components/AnimalSelector.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: {
    AnimalSelector,
  },
});
</script>
