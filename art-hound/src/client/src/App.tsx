import React from 'react'
import './App.css'
import ArtHoundHeader from './components/Header'
import { Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import { LoginProvider } from './components/LoginForm'
import About from './components/About'
import UserProfile from './components/UserProfile'
import Following from './components/Following'
import { Projects } from './components/Projects'
import { AccountCreation } from './components/SignupForm'
import Footer from './components/Footer'
import {
    CreatePost,
    CreateProject,
    EditProfile,
} from './components/PostsAndProjects'

import Search from './components/Search'

function App() {
    return (
        <LoginProvider>
            <div className="app div-body">
                <ArtHoundHeader />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/Home" element={<Home />} />
                    <Route path="/About" element={<About />} />
                    <Route path="/Following" element={<Following />} />
                    <Route path="/Projects" element={<Projects />} />
                    <Route path="/Profile" element={<UserProfile />} />
                    <Route path="/signup" element={<AccountCreation />} />
                    <Route path="/login" element={<Home />} />
                    <Route path="/editProfile" element={<EditProfile />} />
                    <Route path="/createPost" element={<CreatePost />} />
                    <Route path="/createProject" element={<CreateProject />} />
                    <Route path="/Search" element={<Search />} />
                </Routes>
                <Footer />
            </div>
        </LoginProvider>
    )
}

export default App
