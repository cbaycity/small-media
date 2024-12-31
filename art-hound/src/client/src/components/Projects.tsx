import React, { useState, useContext, useEffect } from 'react'
import UserFeed from './Feed'
import { useNavigate } from 'react-router-dom'
import { LoginContext, CheckLogin } from './LoginForm'
import { LeftBar, RightBar } from './Sidebars'

function Projects() {
    const { user, token } = useContext(LoginContext)

    // If not valid login, redirect to Login form.
    const [loginValid, setLoginValid] = useState(true)
    const navigate = useNavigate()
    useEffect(() => {
        const validateLogin = async () => {
            if (token) {
                const isValid = await CheckLogin(token)
                setLoginValid(isValid)
            } else {
                setLoginValid(false)
            }
        }
        validateLogin()
    }, [token])

    useEffect(() => {
        if (!loginValid) {
            // Redirect the user back to /login route
            navigate('/login', { replace: true })
        }
    }, [loginValid, navigate])

    return (
        <>
            <link rel="stylesheet" href="public/feed.css" />
            <div className="center-body general-body-background feed-body">
                <LeftBar />
                <div className="container center-body general-body-background">
                    <p>Need to build the Projects website.</p>
                </div>
                <RightBar />
            </div>
        </>
    )
}

export { Projects }
