import React from "react"

class TheFooter extends React.Component {

    render(){
        return (
            <div id="footer">
                <div>© WhoEverCares {(new Date()).getFullYear()}</div>
            </div>
        )
    }
}

export default TheFooter