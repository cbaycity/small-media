import React, { useContext, useEffect, useState } from 'react'
import UserFeed from './Feed'
import { LeftBar, RightBar } from './Sidebars'
import { LoginContext, CheckLogin } from './LoginForm'
import { useNavigate } from 'react-router-dom'

function UserProfile() {
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
        <div className="container center-body general-body-background feed-body">
            {LeftBar()}
            {UserFeed(user ? user : '', true)}
            {RightBar()}
        </div>
    )
}

export default UserProfile
