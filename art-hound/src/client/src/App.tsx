import React, { useEffect } from 'react'
import './App.css'
import ArtHoundHeader from './components/Header'
import { Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import { LoginProvider } from './components/LoginForm'
import About from './components/About'
import Feed from './components/Feed'
import UserProfile from './components/UserProfile'
import Friends from './components/Friends'
import { AccountCreation } from './components/SignupForm'
import Footer from './components/Footer'
import { CreatePost, CreateProject, EditProfile } from './components/PostForms'

function App() {
    return (
        <LoginProvider>
            <div className="app div-body">
                <ArtHoundHeader />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/Home" element={<Home />} />
                    <Route path="/About" element={<About />} />
                    <Route path="/Friends" element={<Friends />} />
                    <Route path="/Local" element={<Feed />} />
                    <Route path="/Projects" element={<Feed />} />
                    <Route path="/Profile" element={<UserProfile />} />
                    <Route path="/signup" element={<AccountCreation />} />
                    <Route path="/login" element={<Home />} />
                    <Route path="/editProfile" element={<EditProfile />} />
                    <Route path="/createPost" element={<CreatePost />} />
                    <Route path="/createProject" element={<CreateProject />} />
                </Routes>
                <Footer />
            </div>
        </LoginProvider>
    )
}

export default App
