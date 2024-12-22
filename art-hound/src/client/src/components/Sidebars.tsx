import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { NewProjectButton } from './Projects'

const LeftBar = () => {
    const loc = useLocation()
    if (loc.pathname.includes('/Projects')) {
        // Render project related features.
        return NewProjectButton()
    } else {
        return <p>Seattle</p>
    }
}
const RightBar = () => {
    return (
        <div id="right-side-bar" className="side-bar">
            <p>Potential future ad?</p>
        </div>
    )
}

export { LeftBar, RightBar }
