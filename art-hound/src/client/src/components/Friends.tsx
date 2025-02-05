import React, { useState } from 'react'
import { LeftBar, RightBar } from './Sidebars'

function Search() {
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
            const response = await fetch(`/find_user/${username}`, {method: "GET", credentials:"include"})
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
            </div>
            <RightBar />
        </div>
    )
}

export default Search
