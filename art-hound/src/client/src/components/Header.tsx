import React, { useContext, useEffect, useState} from 'react'
import { LoginContext, CheckLogin } from './LoginForm'
import { Link, useNavigate } from 'react-router-dom'

function ArtHoundHeader() {
    let navigate = useNavigate()
    const routeChange = (path: string) => {
        navigate(path)
    }

    const { token, setToken } = useContext(LoginContext);

    const [ isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);
    useEffect( () => {
        const validateLogin = async () => {
            if (token){
                const isValid = await CheckLogin(token);
                setIsLoggedIn(isValid);
            }
            else {
                setIsLoggedIn(false);
            }
        }
        validateLogin()
    }, [token]);

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
                                to="/LocalArt"
                                className="navigation-link px-2 link-two"
                            >
                                Local Art
                            </Link>
                        </li>
                        <li>
                            {' '}
                            <Link
                                to="/PopularArt"
                                className="navigation-link px-2 link-two"
                            >
                                Popular Art
                            </Link>
                        </li>
                        <li>
                            {' '}
                            <Link
                                to="/MyArt"
                                className="navigation-link px-2 link-two"
                            >
                                My Art
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
                        <li>
                            {' '}
                            <Link
                                to="/About"
                                className="navigation-link px-2 link-two"
                            >
                                About
                            </Link>
                        </li>
                    </ul>
                </div>
                { isLoggedIn ? 
                <div className="login headerSection">
                    <button
                        type="button"
                        className="login-button"
                        onClick={() => routeChange('/newPost')}>
                            New Post
                    </button>
                    <button
                        type="button"
                        className="login-button"
                        onClick={() => {setToken("")}}>
                            Sign-Out
                        </button>
                </div>
                :
                <div className="login headerSection">
                    <button
                        type="button"
                        className="login-button"
                        onClick={() => routeChange('/login')}
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
                </div>}
            </header>
        </div>
    )
}

export default ArtHoundHeader
