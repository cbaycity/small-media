import React from 'react'
import { NewProjectButton, NewPostButton } from './PostsAndProjects'

function LeftBar() {
    return (
        <div id="left-side-bar" className="side-bar left-justify">
            <NewProjectButton />
            <br />
            <NewPostButton />
            <link rel="stylesheet" href="/api/public/feed.css" />
        </div>
    )
}
function RightBar() {
    return (
        <div id="right-side-bar" className="side-bar right-justify">
            <p>Potential future ad?</p>
            <link rel="stylesheet" href="/api/public/feed.css" />
        </div>
    )
}

export { LeftBar, RightBar }
