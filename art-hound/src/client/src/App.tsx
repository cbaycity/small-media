import React from 'react';
import './App.css';
import ArtHoundHeader from './components/Header';
import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import About from "./components/About";
import LocalArt from "./components/LocalArt";
import PopularArt from "./components/PopularArt";
import UserProfile from "./components/UserProfile";
import Friends from "./components/Friends";
import { AccountCreation } from "./components/SignupForm";

function App() {
  return (
    <body>
    <div className="app">
      {ArtHoundHeader()}
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/Home" element={<Home />}/>
        <Route path="/About" element={<About />}/>
        <Route path="/Friends" element={<Friends />}/>
        <Route path="/LocalArt" element={<LocalArt />}/>
        <Route path="/PopularArt" element={<PopularArt />}/>
        <Route path="/MyArt" element={<UserProfile />}/>
        <Route path="/signup" element={<AccountCreation />}/>
      </Routes>
    </div>
    </body>
  );
}

export default App;
