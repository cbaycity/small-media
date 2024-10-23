import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import About from "./About";
import LocalArt from "./LocalArt";
import PopularArt from "./PopularArt";
import UserProfile from "./UserProfile";
import Friends from "./Friends";


function artHoundHeader() {
    return(
    <div className="container">
        <header className = "header">
            <div className="logo">
            <img src="/public/artHoundLogo.png" alt="Art Hound Logo"/>
            </div>
            <Router>
                <div className="navigation">
                    <ul className="nav-list">
                        <li> <Link to="/LocalArt" className="navigation-link px-2 link-two">Local Art</Link></li>
                        <li> <Link to="/PopularArt" className="navigation-link px-2 link-two">Popular Art</Link></li>
                        <li> <Link to="/Profile" className="navigation-link px-2 link-two">My Art</Link></li>
                        <li> <Link to="/Friends" className="navigation-link px-2 link-two">Friends</Link></li>
                        <li> <Link to="/About" className="navigation-link px-2 link-two">About</Link></li>
                    </ul>
                </div>
            </Router>
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