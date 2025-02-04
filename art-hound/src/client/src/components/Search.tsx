import React from 'react'
import { LeftBar, RightBar } from './Sidebars'

function Search() {
    return (
        <div className="container center-body general-center-body general-body-background">
            <LeftBar/>
            <div className="general-center-body">
            <h2>Search for a friend's username.</h2>
            </div>
            <RightBar/>
        </div>
    )
}

export default Search
