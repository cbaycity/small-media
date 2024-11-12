import React, { useState, useEffect } from 'react'

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

    return 'Collecting Data'
}

/*
The post should be it's own div that can be spaced out.
Each div should start with a <h3> for the title
<p> for the date
<p> for the verbiage
<img> for the image.


*/

function Feed() {
    return (
        <div className="container center-body general-body-background feed-body">
            <div id="left-side-bar" className="side-bar">
                <p>Seattle</p>
            </div>
            <div id="feed" className="feed">
                <p>{GetFeed('LOCAL', 'cbaycity')}</p>

                <div className="post">
                    <h3>Larch Madness</h3>
                    <p>March 3rd 2024</p>
                    <p>
                        Loved seeing the larches before they lost their leaves.
                    </p>
                    <img className="post-img" src="postphotos/photoOne.jpg" />
                </div>

                <div className="post">
                    <h3>Larch Season</h3>
                    <p>March 3rd 2024</p>
                    <p>Going to see the larches part two.</p>
                    <img className="post-img" src="postphotos/photoTwo.jpg" />
                </div>

                <div className="post">
                    <h3>Testing Image Size.</h3>
                    <p>October 3rd 2024</p>
                    <p>Space Image.</p>
                    <img className="post-img" src="postphotos/photoThree.png" />
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
