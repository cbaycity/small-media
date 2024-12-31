import React from 'react'
import { NewProjectButton, NewPostButton } from './PostsAndProjects'

function LeftBar() {
    return (
        <div id="left-side-bar" className="side-bar left-justify">
            <NewProjectButton />
            <br />
            <NewPostButton />
        </div>
    )
}
function RightBar() {
    return (
        <div id="right-side-bar" className="side-bar right-justify">
            <p>Potential future ad?</p>
        </div>
    )
}

export { LeftBar, RightBar }
