import React, { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function GetFeed(feedType: string, userInfo: string) {
    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch('/feed', {
            method: 'GET',
            headers: {
                USER_INFO: userInfo,
                FEEDTYPE: feedType,
            },
        })
            .then((res) => res.json())
            .then((data) => {
                setData(data)
                console.log(data)
                /* Need to convert the data into objects for the front end to review.*/
            })
    }, [])

    var msg = ''
    if (data !== undefined) {
        msg = 'Still hardcoding posts, work with a DB Bayard'
    } else {
        msg = 'Retrieving Post Data'
    }

    return msg
}

/*
The post should be it's own div that can be spaced out.
Each div should start with a <h3> for the title
<p> for the date
<p> for the verbiage
<img> for the image.


*/

const NewProjectButton = () => {
    let navigate = useNavigate()
    const routeChange = (path: string) => {
        navigate(path)
    }
    return (
        <button
            type="button"
            className="login-button"
            onClick={() => routeChange('/createProject')}
            style={{ padding: '10px', margin: '10px' }}
        >
            New Project
        </button>
    )
}

const LeftBar = () => {
    const loc = useLocation()
    if (loc.pathname.includes('/Projects')) {
        // Render project related features.
        return NewProjectButton()
    } else {
        return <p>Seattle</p>
    }
}

function Feed() {
    return (
        <div className="container center-body general-body-background feed-body">
            <div id="left-side-bar" className="side-bar">
                {LeftBar()}
            </div>
            <div id="feed" className="feed">
                <p>{GetFeed('LOCAL', 'cbaycity')}</p>
                <div className="post">
                    <h3 className="post-header"><span>Larch Madness</span><span>cbaycity</span></h3>
                    <p>March 3rd 2024</p>
                    <p>
                        Loved seeing the larches before they lost their leaves.
                    </p>
                    <img
                        className="post-img"
                        src="postphotos/photoOne.jpg"
                        alt="Larch Post"
                    />
                </div>

                <div className="post">
                    <h3>Larch Season</h3>
                    <p>March 3rd 2024</p>
                    <p>Going to see the larches part two.</p>
                    <img
                        className="post-img"
                        src="postphotos/photoTwo.jpg"
                        alt="Larch Post"
                    />
                </div>

                <div className="post">
                    <h3>Testing Image Size.</h3>
                    <p>October 3rd 2024</p>
                    <p>Space Image.</p>
                    <img
                        className="post-img"
                        src="postphotos/photoThree.png"
                        alt="Planet Post"
                    />
                </div>
            </div>
            <div id="right-side-bar" className="side-bar">
                <p>Ad</p>
            </div>
            <link rel="stylesheet" href="public/feed.css" />
        </div>
    )
}

export default Feed
