import React, { useContext, useState, useEffect } from 'react'
import { LoginContext, LoginForm, CheckLogin } from './LoginForm'

function Home() {
    const { user, storeUser, token, storeToken, logOut } =
        useContext(LoginContext)

    const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null)
    useEffect(() => {
        const validateLogin = async () => {
            if (token) {
                const isValid = await CheckLogin(token)
                setIsLoggedIn(isValid)
            } else {
                setIsLoggedIn(false)
            }
        }
        validateLogin()
    }, [token])

    return (
        <div className="container center-body">
            {!isLoggedIn ? (
                <LoginForm />
            ) : (
                <p>Need to build the Home website.</p>
            )}
        </div>
    )
}

export default Home
