import React from 'react';
import { Link, useNavigate } from "react-router-dom";


function ArtHoundHeader() {
    
    let navigate = useNavigate();
    const routeChange = (path:string) =>{ 
        navigate(path);
      }
    
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
                <button type="button" className="login-button" onClick={() => routeChange("/login")}>Login</button>
                <button type="button" className="login-button" onClick={() => routeChange("/signup")}>Sign-Up</button>
            </div>
        </header>
    </div>
    );
};

export default ArtHoundHeader;