import React, { useState, useEffect } from 'react'
import { LeftBar, RightBar } from './Sidebars'
import { Link } from 'react-router-dom'

function FriendsSection() {
    const [friends, setFriends] = useState([])
    useEffect(() => {
        const query_friends = async () => {
            try {
                const response = await fetch('/friendlist', {
                    method: 'GET',
                    credentials: 'include',
                })
                if (response.ok) {
                    const data = await response.json()
                    setFriends(data)
                } else {
                    setFriends([])
                }
            } catch (error) {
                if (error instanceof Error) {
                    console.error(
                        'Failed to fetch Friend List. ',
                        error.message
                    )
                } else {
                    console.error('Failed to get Friend List.', error)
                }
            }
        }
        query_friends()
    }, [])

    return (
        <div>
            {friends.map((friend, i) => (
                <div className="friend-block" key={i}>
                    <Link to={`/Profile/${friend}`} className="project-link">
                        <p>{friend}</p>
                    </Link>
                </div>
            ))}
        </div>
    )
}

function _FriendButton(curr_status: boolean){
    const [ friendBool, setFriendBool ] = useState(curr_status)

    const click = (status) => {
        if (status == true){
            // If friends, call the backend to not be friends.

        }
        else {
            // They're not friends, so add friend.
        }
    }

}

function GetRequests() {
    const [requests, setRequests] = useState([])
    useEffect(() => {
        const getFriendRequests = async () => {
            try {
                const response = await fetch('/friend_requests', {
                    method: 'GET',
                    credentials: 'include',
                })
                if (response.ok) {
                    const data = await response.json()
                    setRequests(data)
                } else {
                    setRequests([])
                }
            } catch (error) {
                if (error instanceof Error) {
                    console.error(
                        'Failed to fetch Friend Requests. ',
                        error.message
                    )
                } else {
                    console.error('Failed to fetch friend requests.', error)
                }
            }
        }
        getFriendRequests()
    }, [])

    // return friend requests and a button to click add friend.
    return (
        <div>
            {requests.map((request, i) => (
                <div className="friend-block" key={i}>
                    <p>{request}</p> <button className="login-button friend-button">Add Friend</button>
                </div>
            ))}
        </div>
    )
}

function Friends() {
    const [submitSuccess, setSubmitSuccess] = useState(false)
    const [madeSubmission, setMadeSubmission] = useState(false)
    const [alreadyFriends, setAlreadyFriends] = useState(false)

    const handleSubmit = async (formEvent: React.FormEvent) => {
        formEvent.preventDefault()

        const form = formEvent.target as HTMLFormElement
        const htmlUsername = form.elements.namedItem(
            'username-search'
        ) as HTMLInputElement
        const username = htmlUsername.value.trim()

        try {
            const response = await fetch(`/find_user/${username}`, {
                method: 'GET',
                credentials: 'include',
            })
            if (response.ok) {
                const data = await response.json()
                if (data['AddedFriend']) {
                    setSubmitSuccess(true)
                    setMadeSubmission(true)
                    setAlreadyFriends(false)
                } else if (data['AlreadyFriend']) {
                    setSubmitSuccess(true)
                    setMadeSubmission(true)
                    setAlreadyFriends(true)
                } else {
                    setSubmitSuccess(false)
                    setMadeSubmission(true)
                    setAlreadyFriends(false)
                }
            } else {
                setSubmitSuccess(false)
                setMadeSubmission(true)
            }
        } catch (error) {
            console.error('Error fetching data', error)
            setSubmitSuccess(false)
            setMadeSubmission(true)
        }
    }

    return (
        <div className="container center-body general-center-body general-body-background">
            <LeftBar />
            <div className="general-center-body basic-padding column-flex">
                {(() => {
                    if (!submitSuccess && madeSubmission) {
                        return <p>Invalid username, exact spelling required.</p>
                    } else if (
                        submitSuccess &&
                        madeSubmission &&
                        !alreadyFriends
                    ) {
                        return <p>Friend Request Sent.</p>
                    } else if (
                        submitSuccess &&
                        madeSubmission &&
                        alreadyFriends
                    ) {
                        return <p>You're already friends!</p>
                    }
                    return null
                })()}
                <h2>Friend's Username:</h2>
                <form className="signup-form" onSubmit={handleSubmit}>
                    <label htmlFor="username-search">
                        <input
                            type="text"
                            id="username-search"
                            name="username-search"
                            required
                        />
                    </label>
                </form>
                <div>
                    <h2>Friend Requests:</h2>
                    <GetRequests />
                </div>
                <div>
                    <h2>Current Friends:</h2>
                    {<FriendsSection />}
                </div>
            </div>
            <RightBar />
        </div>
    )
}

export default Friends
