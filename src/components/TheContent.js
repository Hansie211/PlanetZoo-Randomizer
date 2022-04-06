import React from "react"
import AnimalSpotlight from "./AnimalSpotlight/AnimalSpotlight"
import Button from "./Button/Button"

class TheContent extends React.Component {

    constructor(props){
        super(props)

        this.state = {
            selectedAnimalId: this.getRandomItem(this.getRepository().allAnimals.keys),
        }

        this.handleClickRegion = this.handleClickRegion.bind(this)
        this.handleClickBiome = this.handleClickBiome.bind(this)
        this.handleClickHabitat = this.handleClickHabitat.bind(this)
        this.handleClickRandom = this.handleClickRandom.bind(this)
    }

    /** @return {import("../data/repository").Repository} */
    getRepository(){
        const { repo } = this.props
        return repo
    }

    setAnimal(animal){

        const animalId = this.getRepository().allAnimals.getKey(animal)
        this.setState( {selectedAnimalId: animalId } )
    }

    getRandomItem( list ) {
        const index = Math.floor( Math.random() * list.length )
        return list[index]
    }

    getRegionButtons(regions){

        const list = regions.map( (region, id) => { return {
            region, id,
        }})

        list.sort( (a,b) => {
            const itemA = a.region
            const itemB = b.region

            return itemA.Name > itemB.Name
         } )

        return list.map( (item) => {
            const { region, id, } = item
            return <Button key={id} title={region.Name} onClick={this.handleClickRegion} dataTag={id} />
         })
    }

    getBiomeButtons(biomes){
        const list = biomes.map( (biome, id) => { return {
            biome, id,
        }})

        list.sort( (a,b) => {
            const itemA = a.biome
            const itemB = b.biome

            return itemA.Name > itemB.Name
         } )

        return list.map( (item) => {
            const { biome, id, } = item
            return <Button key={id} title={biome.Name} onClick={this.handleClickBiome} dataTag={id} />
        })
    }

    handleClickRegion(event){
        const element = event.currentTarget
        const tag = element.dataset["tag"]

        const region = this.getRepository().allRegions.get(tag)
        const animal = this.getRandomItem( region.Animals )

        this.setAnimal(animal)
    }

    handleClickBiome(event){
        const element = event.currentTarget
        const tag = element.dataset["tag"]

        const biome = this.getRepository().allBiomes.get(tag)
        const animal = this.getRandomItem( biome.Animals )

        this.setAnimal(animal)
    }

    handleClickHabitat(event){
        const element = event.currentTarget
        const tag = element.dataset["tag"]

        const isHabitatAnimal = (tag === "habitat")
        const animalList = this.getRepository().allAnimals.filter( (animal) => animal.isExhibit !== isHabitatAnimal )
        const animal = this.getRandomItem( animalList )

        this.setAnimal(animal)
    }

    handleClickRandom(event){

        const animal = this.getRandomItem( this.getRepository().allAnimals.values )

        this.setAnimal(animal)
    }

    render(){
        const repo = this.getRepository()
        const selectedAnimal = repo.allAnimals.get(this.state.selectedAnimalId)

        return (
            <div id="content">
                <div>Your animal:</div>
                <AnimalSpotlight animal={selectedAnimal} />
                <div id="button-container">
                    <div className="button-row">
                        <Button title="Random" onClick={this.handleClickRandom} />
                        <Button title="Habitat" dataTag="habitat" onClick={this.handleClickHabitat} />
                        <Button title="Exhibit" dataTag="exhibit" onClick={this.handleClickHabitat} />
                    </div>
                    <div className="button-row">
                        { this.getRegionButtons(repo.allRegions) }
                    </div>
                    <div className="button-row">
                        { this.getBiomeButtons(repo.allBiomes) }
                    </div>
                </div>
            </div>
        )
    }
}

export default TheContent