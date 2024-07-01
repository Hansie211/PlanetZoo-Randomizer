<template>
  <q-page class="row items-center justify-evenly">
    <div id="box" style="max-width: 1000px; background-color: rgb(64, 69, 72); padding: 10px; border-radius: 5px">
      <animal-selector />
    </div>

    <img src="~/assets/screenshot_1.jpg" style="position: fixed; z-index: -1; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; filter: blur(2px)" />
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

<style scoped>
@media (min-width: 1050px) {
  #box {
    width: 1000px;
  }
}
</style>
