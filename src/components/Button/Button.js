import React from "react"
import "./Button.css"

class Button extends React.Component {

    render(){

        const { title, onClick, dataTag, } = this.props

        return (
            <div className="button" onClick={onClick} data-tag={dataTag}>{title}</div>
        )
    }
}

export default Button