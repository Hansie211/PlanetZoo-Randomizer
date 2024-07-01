<template>
  <div style="width: 1000px">
    <animal-card :animal="currentAnimal" :index="currentAnimalIndex + 1" :max="animals.length" @click-randomize="randomAnimal" @click-next="nextAnimal" @click-previous="previousAnimal" />
    <animal-filter @on-filter-updated="updateFilter" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { getAnimalRepo } from 'src/data/AnimalRepo';
import AnimalFilter from './AnimalFilter.vue';
import { AnimalDTO } from 'src/data/animal';
import AnimalCard from './AnimalCard.vue';

export default defineComponent({
  components: { AnimalFilter, AnimalCard },

  setup() {
    const animalRepo = getAnimalRepo();
    const animals = ref(animalRepo.getAll());
    const currentAnimalIndex = ref(0);

    return {
      animalRepo,
      animals,
      currentAnimalIndex,
    };
  },

  computed: {
    currentAnimal() {
      this.currentAnimalIndex;
      this.animals;

      return this.animals[this.currentAnimalIndex];
    },
  },

  methods: {
    randomAnimal() {
      const nindex = Math.max(0, Math.floor(Math.random() * this.animals.length) - 1);
      this.currentAnimalIndex = nindex >= this.currentAnimalIndex ? nindex + 1 : nindex;
    },

    nextAnimal() {
      this.currentAnimalIndex = (this.currentAnimalIndex + 1) % this.animals.length;
    },

    previousAnimal() {
      this.currentAnimalIndex--;
      if (this.currentAnimalIndex < 0) {
        this.currentAnimalIndex = this.animals.length - 1;
      }
    },

    updateFilter(filter: (a: AnimalDTO) => boolean) {
      this.animals = this.animalRepo.getAll().filter(filter);
      this.randomAnimal();
    },
  },
});
</script>
