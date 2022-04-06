import React from "react"
import "./AnimalSpotlight.css"

class AnimalSpotlight extends React.Component {

    render(){

        /** @type {{animal: import("../../data/repository").Animal}} */
        const { animal } = this.props

        if (animal === undefined)
            return null

        return (
            <div id="animal-spotlight-row">
                <div id="animal-spotlight-space"></div>
                <div id="animal-spotlight">{animal.Name}</div>
                <div id="animal-data">
                    <div className="data-row"><span>Regions: </span>{animal.Regions.map( x => x.Name).join(", ")}</div>
                    <div className="data-row"><span>Biomes: </span>{animal.Biomes.map( x => x.Name).join(", ")}</div>
                </div>
            </div>
        )
    }
}

export default AnimalSpotlight

