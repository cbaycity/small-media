import React from 'react';

function artHoundHeader() {
    return(
    <div className="container">
        <header className = "header">
            <div className="logo">
            <img src="/public/artHoundLogo.png" alt="Art Hound Logo"/>
            </div>
            <div className="navigation">
            <ul className="nav-list">
                <li> <a href="LocalArt" className="navigation-link px-2 link-two">Local Art</a></li>
                <li> <a href="PopularArt" className="navigation-link px-2 link-two">Popular Art</a></li>
                <li> <a href="profile" className="navigation-link px-2 link-two">My Art</a></li>
                <li> <a href="friends" className="navigation-link px-2 link-two">Friends</a></li>
                <li> <a href="about" className="navigation-link px-2 link-two">About</a></li>
            </ul>
            </div>
            <div className="login">
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