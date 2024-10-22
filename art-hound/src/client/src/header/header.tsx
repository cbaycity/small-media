import React from 'react';

function artHoundHeader() {
    return(
    <div className="container">
        <header className = "d-flex align-items-center justify-content-mb-between py-3 mb-4 border-bottom">
            <div className="logo d-flex align-items-center">
            <img src="/public/artHoundLogo.png" alt="Art Hound Logo" className="d-flex align-items-center App-logo"/>
            </div>
            <div className="align-items-center">
            <ul className="navigation ul mb-2 justify-content-center">
                <li> <a href="LocalArt" className="navigation-link px-2 link-two">Local Art</a></li>
                <li> <a href="PopularArt" className="navigation-link px-2 link-two">Popular Art</a></li>
                <li> <a href="profile" className="navigation-link px-2 link-two">My Art</a></li>
                <li> <a href="friends" className="navigation-link px-2 link-two">Friends</a></li>
                <li> <a href="about" className="navigation-link px-2 link-two">About</a></li>
            </ul>
            </div>
            <div className="d-flex button-right">
                <button type="button" className="btn btn-outline-primary me-2">Login</button>
                <button type="button" className="btn btn-primary">Sign-Up</button>
            </div>
        </header>
    </div>
    );
};

export default artHoundHeader;