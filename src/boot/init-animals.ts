import { boot } from 'quasar/wrappers';
import { Repo } from 'src/data/repo';
import { AnimalDTO } from 'src/data/animal';
import { setAnimalRepo } from 'src/data/AnimalRepo';

import animal_data from 'src/data/store/animals.json';

export default boot(async () => {
  const repo: Repo<AnimalDTO> = new Repo(animal_data.map((data) => Object.assign(new AnimalDTO(), data)).sort((a, b) => a.title.localeCompare(b.title)));
  setAnimalRepo(repo);
});
