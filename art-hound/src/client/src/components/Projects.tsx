import React, { useState, useContext, useEffect } from 'react'
import UserFeed from './Feed'
import { useNavigate } from 'react-router-dom'
import { LoginContext, CheckLogin } from './LoginForm'

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
        <div className="container center-body general-body-background">
            <p>Need to build the Projects website.</p>
        </div>
    )
}

export { Projects }
