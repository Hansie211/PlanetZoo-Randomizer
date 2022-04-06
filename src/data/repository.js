import RegionsData from "./regions.json"
import BiomesData from "./biomes.json"
import AnimalsData from "./animals.json"

import Dictionary from "./dictionary"

/**
 * @typedef {Object} AnimalModel
 * @property {Number} id
 * @property {String} name
 * @property {Boolean} is_exhibit_animal
 * @property {Array<Number>} regions
 * @property {Array<Number>} biomes
 */

/**
 * @typedef {Object} BiomeModel
 * @property {Number}     id
 * @property {String}     name
 */

/**
 * @typedef {Object} RegionModel
 * @property {Number}     id
 * @property {String}     name
 */

/**
 * @callback GetAnimals
 * @returns {Array<Animal>}
 */

/**
 * @typedef {Object} Animal
 * @property {String} Name
 * @property {Array<Biome>} Biomes
 * @property {Array<Region>} Regions
 * @property {Boolean} isExhibit
 */

/**
 * @typedef {Object} Region
 *
 * @property {String} Name
 * @property {Array<Animal>} Animals
 */

/**
 * @typedef {Object} Biome
 *
 * @property {String} Name
 * @property {Array<Animal>} Animals
 */

export class Repository {

    /** @type {Dictionary.<Number, Biome>} */
    allBiomes = new Dictionary()
    /** @type {Dictionary.<Number, Region>} */
    allRegions = new Dictionary()
    /** @type {Dictionary.<Number, Animal>} */
    allAnimals = new Dictionary()

    init(){

        /** @param {BiomeModel} model */
        const mapBiomeModel = (model) => {

            /** @type {Biome} */
            const result = {
                Name: model.name,
                Animals: [],
            }

            return result
        }

        /** @param {RegionModel} model */
        const mapRegionModel = (model) => {

            /** @type {Region} */
            const result = {
                Name: model.name,
                Animals: [],
            }

            return result
        }

        /** @param {AnimalModel} model */
        const mapAnimalModel = (model) => {

            const biomeIds = Array.isArray(model.biomes) ? model.biomes : []
            const regionIds = Array.isArray(model.regions) ? model.regions : []

            /** @type {Animal} */
            const result = {
                Name: model.name,
                isExhibit: model.is_exhibit_animal,
                Biomes: biomeIds.map( (id) => this.allBiomes.get(id) ),
                Regions: regionIds.map( (id) => this.allRegions.get(id) ),
            }

            result.Biomes.forEach( (obj) => obj.Animals.push(result) )
            result.Regions.forEach( (obj) => obj.Animals.push(result) )

            return result
        }

        this.allBiomes.import(BiomesData, x => x.id, mapBiomeModel)
        this.allRegions.import(RegionsData, x => x.id, mapRegionModel)
        this.allAnimals.import(AnimalsData, x => x.id, mapAnimalModel)
    }

    constructor(){

        this.init()
    }
}

export default Repository
