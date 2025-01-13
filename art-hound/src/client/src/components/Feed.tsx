import React, { useState, useEffect, useContext } from 'react'
import { LoginContext } from './LoginForm'

export interface PostData {
    title: string
    username: string
    startDate: string
    endDate: string
    description: string
    image_id: string
    project: string
    project_id: string
}

function UserFeed(username: string, onUserProfile: boolean = false) {
    // Need to get data from /getUserPosts/<username>, pass the token as data.

    const [postsList, setPostsList] = useState<PostData[]>([])
    // Create a list of posts which has dictionaries of the post.
    const { token, user } = useContext(LoginContext)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await fetch(`/getUserPosts/${username}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: token }),
                })

                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`)
                }

                const data = await response.json()
                setPostsList(data)
            } catch (err: any) {
                setError(err.message || 'An error occurred.')
            }
        }

        if (username) {
            fetchPosts()
        }
    }, [username, token])

    if (error) {
        return <div>Error: {error}</div>
    }

    const today = new Date()

    return (
        <>
            <div id="feed" className="feed">
                {postsList && postsList.length > 0 ? (
                    postsList.map((post, index) => (
                        <div className="post" key={index}>
                            <h3>{post['title']}</h3>
                            <p>{post['project']}</p>
                            <p>
                                {post['startDate'] === post['endDate']
                                    ? post['startDate']
                                    : `${post['startDate']} - ${post['endDate']}`}
                            </p>
                            <p>{post['description']}</p>
                            <img
                                className="post-img"
                                src={`/postphotos/${post['image_id']}/${token}`}
                                alt="Photo from post."
                            />
                        </div>
                    ))
                ) : (
                    // No Posts to display
                    <div className="post">
                        <h3 className="post-header">
                            <span>No Posts to Display</span>
                            <span>{user}</span>
                        </h3>
                        <p>
                            {today.toLocaleDateString('en-US', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                            })}
                        </p>
                        <p>
                            {onUserProfile
                                ? 'Add some of your own posts to see data here!'
                                : `Add some friends of your own to see posts here!
                            This website's found, username cbaycity, is public and can be a friend.`}
                        </p>
                        <img
                            className="post-img"
                            src="/public/artHoundLogoColor.svg"
                            alt="Art Hound Logo"
                        />
                    </div>
                )}
            </div>
            <link rel="stylesheet" href="public/feed.css" />
        </>
    )
}

export default UserFeed
