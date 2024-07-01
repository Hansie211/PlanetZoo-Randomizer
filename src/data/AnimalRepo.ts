import { Repo } from './repo';
import { AnimalDTO } from './animal';

let animalRepo!: Repo<AnimalDTO>;

export function setAnimalRepo(repo: Repo<AnimalDTO>) {
  animalRepo = repo;
}

export function getAnimalRepo(): Repo<AnimalDTO> {
  return animalRepo;
}
