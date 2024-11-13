import React from 'react'
import './App.css'
import ArtHoundHeader from './components/Header'
import { Routes, Route } from 'react-router-dom'
import { Home, Login } from './components/Home'
import About from './components/About'
import Feed from './components/Feed'
import UserProfile from './components/UserProfile'
import Friends from './components/Friends'
import { AccountCreation, ProfileCreation } from './components/SignupForm'

function App() {
    return (
        <div className="app div-body">
            {ArtHoundHeader()}
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/Home" element={<Home />} />
                <Route path="/About" element={<About />} />
                <Route path="/Friends" element={<Friends />} />
                <Route path="/LocalArt" element={<Feed />} />
                <Route path="/PopularArt" element={<Feed />} />
                <Route path="/MyArt" element={<UserProfile />} />
                <Route path="/signup" element={<AccountCreation />} />
                <Route path="/login" element={<Login />} />
                <Route path="/createAccount" element={<ProfileCreation />} />
            </Routes>
        </div>
    )
}

export default App
