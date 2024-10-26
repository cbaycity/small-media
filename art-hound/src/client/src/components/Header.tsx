import React from 'react';
import { Link } from "react-router-dom"


function artHoundHeader() {
    return(
    <div className="container">
        <header className = "header" id="header">
            <div className="logo headerSection">
            <img src="/public/artHoundLogo.svg" alt="Art Hound Logo" width="150px" height="90px"/>
            </div>
            <div className="navigation headerSection">
                <ul className="nav-list">
                    <li> <Link to="/LocalArt" className="navigation-link px-2 link-two">Local Art</Link></li>
                    <li> <Link to="/PopularArt" className="navigation-link px-2 link-two">Popular Art</Link></li>
                    <li> <Link to="/MyArt" className="navigation-link px-2 link-two">My Art</Link></li>
                    <li> <Link to="/Friends" className="navigation-link px-2 link-two">Friends</Link></li>
                    <li> <Link to="/About" className="navigation-link px-2 link-two">About</Link></li>
                </ul>
            </div>
            <div className="login headerSection">
                <div className="login-button">
                <button type="button" className="login-button">Login</button>
                </div>
                <div className="login-button">
                <button type="button" className="login-button">Sign-Up</button>
                </div>
            </div>
        </header>
    </div>
    );
};

export default artHoundHeader;