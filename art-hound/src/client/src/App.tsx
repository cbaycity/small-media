import React, { useState, useEffect } from 'react';
import './App.css';
import artHoundHeader from './components/Header';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./components/Home";
import About from "./components/About";
import LocalArt from "./components/LocalArt";
import PopularArt from "./components/PopularArt";
import UserProfile from "./components/UserProfile";
import Friends from "./components/Friends";


function App() {
  return (
    <div className="app">
      {artHoundHeader()}
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/Home" element={<Home />}/>
        <Route path="/About" element={<About />}/>
        <Route path="/Friends" element={<Friends />}/>
        <Route path="/LocalArt" element={<LocalArt />}/>
        <Route path="/PopularArt" element={<PopularArt />}/>
        <Route path="/MyArt" element={<UserProfile />}/>
      </Routes>
    </div>
  );
}

export default App;
