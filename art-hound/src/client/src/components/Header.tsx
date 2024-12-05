import React, { useContext, useEffect, useState } from 'react'
import { LoginContext, CheckLogin } from './LoginForm'
import { Link, useNavigate } from 'react-router-dom'

function ArtHoundHeader() {
    let navigate = useNavigate()
    const routeChange = (path: string) => {
        navigate(path)
    }

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
        <div className="container">
            <header className="header" id="header">
                <div className="logo headerSection">
                    <img
                        src="/public/artHoundLogoColor.svg"
                        alt="Art Hound Logo"
                        width="150px"
                        height="90px"
                    />
                </div>
                <div className="navigation headerSection">
                    <ul className="nav-list">
                        <li>
                            {' '}
                            <Link
                                to="/Local"
                                className="navigation-link px-2 link-two"
                            >
                                Local
                            </Link>
                        </li>
                        <li>
                            {' '}
                            <Link
                                to="/Projects"
                                className="navigation-link px-2 link-two"
                            >
                                Projects
                            </Link>
                        </li>
                        <li>
                            {' '}
                            <Link
                                to="/Profile"
                                className="navigation-link px-2 link-two"
                            >
                                Profile
                            </Link>
                        </li>
                        <li>
                            {' '}
                            <Link
                                to="/Friends"
                                className="navigation-link px-2 link-two"
                            >
                                Friends
                            </Link>
                        </li>
                    </ul>
                </div>
                {isLoggedIn ? (
                    <div className="login headerSection">
                        <button
                            type="button"
                            className="login-button"
                            onClick={() => routeChange('/createPost')}
                        >
                            New Post
                        </button>
                        <button
                            type="button"
                            className="login-button"
                            onClick={() => {
                                logOut()
                            }}
                        >
                            Sign-Out
                        </button>
                    </div>
                ) : (
                    <div className="login headerSection">
                        <button
                            type="button"
                            className="login-button"
                            onClick={() => {
                                routeChange('/login')
                            }}
                        >
                            Login
                        </button>
                        <button
                            type="button"
                            className="login-button"
                            onClick={() => routeChange('/signup')}
                        >
                            Sign-Up
                        </button>
                    </div>
                )}
            </header>
        </div>
    )
}

export default ArtHoundHeader
