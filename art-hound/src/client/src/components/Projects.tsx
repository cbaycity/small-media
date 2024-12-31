import React, { useState, useContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LoginContext, CheckLogin } from './LoginForm'
import { LeftBar, RightBar } from './Sidebars'

interface Project {
    title: string
    username: string
    startDate: string
    endDate: string
    description: string
    'image-id': string | null
}

function DisplayProject(project: Project, token: string | null, index: number) {
    return (
        <div className="project" key={index}>
            <h3>{project['title']}</h3>
            <p>Owner: {project['username']}</p>
            <p>
                {project['startDate'] === project['endDate']
                    ? project['startDate']
                    : `${project['startDate']} - ${project['endDate']}`}
            </p>
            <p>{project['description']}</p>
            {project['image-id'] && token ? (
                <img
                    className="project-img"
                    src={`/postphotos/${project['image-id']}/${token}`}
                    alt="Main project photo."
                />
            ) : (
                <></>
            )}
        </div>
    )
}

function DisplayListProjects(projects: Project[], token: string | null) {
    return (
        <div id="feed" className="feed">
            {projects && projects.length > 0 ? (
                projects.map((project, index) =>
                    DisplayProject(project, token, index)
                )
            ) : (
                <p>
                    Create some projects and consider following a friend's
                    projects.
                </p>
            )}
        </div>
    )
}

function Projects() {
    const [userProjects, setUserProjects] = useState<Project[]>([])
    const { user, token } = useContext(LoginContext)
    const [error, setError] = useState<string | null>(null)

    // If not valid login, redirect to Login form.
    const [loginValid, setLoginValid] = useState(true)
    const navigate = useNavigate()
    useEffect(() => {
        const validateLogin = async () => {
            if (token) {
                const isValid = await CheckLogin(token)
                setLoginValid(isValid)
            } else {
                setLoginValid(false)
            }
        }
        validateLogin()
    }, [token])

    useEffect(() => {
        if (!loginValid) {
            // Redirect the user back to /login route
            navigate('/login', { replace: true })
        }
    }, [loginValid, navigate])

    // Gets a User's projects list.
    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await fetch(`/UserProjects`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: token }),
                })

                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`)
                }

                const data = await response.json()
                setUserProjects(data)
            } catch (err: any) {
                setError(err.message || 'An error occurred.')
            }
        }

        if (user) {
            fetchProjects()
        }
    }, [user, token])

    return (
        <>
            <link rel="stylesheet" href="public/feed.css" />
            <div className="center-body general-body-background feed-body">
                <LeftBar />
                <div className="container center-body general-body-background">
                    <div className="UserProjects">
                        {DisplayListProjects(userProjects, token)}
                    </div>
                    <div className="OtherProjects">
                        <p>Other users projects feed is under development.</p>
                    </div>
                </div>
                <RightBar />
            </div>
        </>
    )
}

export { Projects }
