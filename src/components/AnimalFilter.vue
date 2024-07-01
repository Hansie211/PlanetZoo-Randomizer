<template>
  <div id="box" style="width: 100%">
    <filter-group title="Habitat" :labels="['Exhibit', 'Habitat']" :options="habitats" @on-update-values="(e) => (allowed_habitats = e)" />
    <filter-group title="Biome" :options="biomes" @on-update-values="(e) => (allowed_biomes = e)" />
    <filter-group title="Continent" :options="continents" @on-update-values="(e) => (allowed_continents = e)" />
    <filter-group title="DLC" :options="dlcs" @on-update-values="(e) => (allowed_dlcs = e)" />
  </div>
</template>

<script lang="ts">
import { AnimalDTO } from 'src/data/animal';
import { defineComponent, ref, Ref } from 'vue';
import { getAnimalRepo } from 'src/data/AnimalRepo';
import FilterGroup from './FilterGroup.vue';

export default defineComponent({
  emits: ['onFilterUpdated'],
  components: { FilterGroup },
  setup() {
    const animalRepo = getAnimalRepo();

    const habitats = ['Exhibit', 'Full'];
    const biomes = [...new Set(animalRepo.getAll().flatMap((a) => a.biomes))].sort();
    const continents = [...new Set(animalRepo.getAll().flatMap((a) => a.continents))].sort();
    const dlcs = [...new Set(animalRepo.getAll().map((a) => a.edition))].sort();

    const allowed_habitats: Ref<string[]> = ref([...habitats]);
    const allowed_biomes: Ref<string[]> = ref([...biomes]);
    const allowed_continents: Ref<string[]> = ref([...continents]);
    const allowed_dlcs: Ref<string[]> = ref([...dlcs]);

    return {
      habitats,
      biomes,
      dlcs,
      continents,

      allowed_habitats,
      allowed_biomes,
      allowed_continents,
      allowed_dlcs,
    };
  },

  computed: {
    currentFilter() {
      this.allowed_habitats.length;
      this.allowed_biomes.length;
      this.allowed_continents.length;
      this.allowed_dlcs.length;

      return (animal: AnimalDTO) =>
        this.allowed_habitats.includes(animal.interactivity) &&
        animal.biomes.find((v) => this.allowed_biomes.includes(v)) !== undefined &&
        animal.continents.find((v) => this.allowed_continents.includes(v)) !== undefined &&
        this.allowed_dlcs.includes(animal.edition);
    },
  },

  watch: {
    currentFilter: function (nval) {
      this.$emit('onFilterUpdated', nval);
    },
  },
});
</script>
