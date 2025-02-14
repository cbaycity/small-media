import React, { useState, useEffect, useContext } from 'react'
import { LoginContext } from './LoginForm'
import { LeftBar, RightBar } from './Sidebars'
import { Link } from 'react-router-dom'

function FriendButton({
    curr_status,
    target_user,
}: {
    curr_status: boolean
    target_user: string
}) {
    const [friendBool, setFriendBool] = useState(curr_status)
    const [addOrRemove, setAddOrRemove] = useState('')
    const { token } = useContext(LoginContext)

    useEffect(() => {
        if (friendBool == true) {
            setAddOrRemove('remove')
        } else {
            setAddOrRemove('add')
        }
    }, [])

    const click = () => {
        const update_friend = async () => {
            // If friends, call the backend to not be friends.
            try {
                const response = await fetch(`process_friend_request`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        token: token,
                        target_user: target_user,
                        add_or_remove: addOrRemove,
                    }),
                })
                if (response.ok) {
                    setFriendBool(!friendBool)
                }
            } catch (err: any) {
                console.error(err.message || 'Backend Call Issue.')
            }
        }
        update_friend()
    }
    return (
        <button
            className="login-button friend-button"
            style={friendBool ? { backgroundColor: '#B22222' } : {}}
            onClick={click}
        >
            {friendBool ? 'Remove Friend' : 'Add Friend'}
        </button>
    )
}

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
                    <FriendButton curr_status={true} target_user={friend} />
                </div>
            ))}
        </div>
    )
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
            {requests.map((requester_name, i) => (
                <div className="friend-block" key={i}>
                    <p>{requester_name}</p>{' '}
                    <FriendButton
                        curr_status={false}
                        target_user={requester_name}
                    />
                </div>
            ))}
        </div>
    )
}

function Friends() {
    const [submitSuccess, setSubmitSuccess] = useState(false)
    const [madeSubmission, setMadeSubmission] = useState(false)
    const [alreadyFriends, setAlreadyFriends] = useState(false)

    const { token } = useContext(LoginContext)

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
                body: JSON.stringify({
                    token: token,
                }),
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
                <h2>Add Friend (username):</h2>
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
