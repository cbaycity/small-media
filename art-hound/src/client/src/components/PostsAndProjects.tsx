// A File containing forms for post creation, project creation, and profile creation.

import react, { useState, useContext, useEffect } from 'react'
import { LoginContext } from './LoginForm'
import { useNavigate } from 'react-router-dom'

var counter = 0

const addFormCss = () => {
    return (
        <>
            <link rel="stylesheet" href="public/basic-form.css" />
        </>
    )
}

const AddDateFields = () => {
    const today = new Date().toISOString().split('T')[0] // Format date as yyyy-mm-dd
    const [startDate, setStartDate] = useState(today)
    const [endDate, setEndDate] = useState(today)
    return (
        <>
            <label htmlFor="start-date">
                Start Date:
                <input
                    type="date"
                    id="start-date"
                    name="start-date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    required
                />
            </label>
            <label htmlFor="end-date">
                End Date:
                <input
                    type="date"
                    id="end-date"
                    name="end-date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </label>
        </>
    )
}

function CreatePost() {
    const { token } = useContext(LoginContext)
    const [projectList, setProjectList] = useState([])
    const [selectedProject, setSelectedProject] = useState('')
    useEffect(() => {
        counter += 1
        console.log('Call Counter at ', counter)
        console.log('token: ', token)
        if (!token) {
            console.log('Token not set, not calling lookup')
            return
        }
        const fetchData = async () => {
            try {
                const response = await fetch('/UserProjects', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: token }),
                })

                if (!response.ok) {
                    const errorText = await response.text()
                    throw new Error(`Error ${response.status}: ${errorText}`)
                }

                const projects = await response.json()
                setProjectList(projects) // Update project list
            } catch (error) {
                if (error instanceof Error) {
                    // Narrowing the type
                    console.error('Failed to fetch projects:', error.message)
                } else {
                    console.error('An unexpected error occurred', error)
                }
            }
        }

        fetchData()
    }, [token]) // Dependency array ensures this runs when token changes

    const handleSelectionChange = (
        event: React.ChangeEvent<HTMLSelectElement>
    ) => {
        setSelectedProject(event.target.value)
    }

    return (
        <>
            {addFormCss()}
            <div className="container full-height general-body-background">
                <div className="form-container full-height">
                    <div id="form-one-block">
                        <form
                            className="signup-form"
                            action="/createPost"
                            method="post"
                            encType="multipart/form-data"
                        >
                            <label htmlFor="title">
                                Post Title
                                <input
                                    type="text"
                                    id="title"
                                    name="title"
                                    autoComplete="off"
                                    required
                                    maxLength={30}
                                />
                            </label>
                            {AddDateFields()}
                            <label htmlFor="description">
                                Post Description
                                <input
                                    type="text"
                                    id="description"
                                    name="description"
                                    autoComplete="off"
                                    required
                                    maxLength={160}
                                />
                            </label>
                            <label htmlFor="project">Related Project</label>
                            <select
                                id="project"
                                value={selectedProject}
                                onChange={handleSelectionChange}
                                required
                            >
                                <option value="" disabled>
                                    -- Select a Project --
                                </option>
                                {projectList.map((project, index) => (
                                    <option key={index} value={project}>
                                        {project}
                                    </option>
                                ))}
                            </select>
                            <br />
                            <label htmlFor="post-image">
                                Post Photo:
                                <input
                                    id="post-image"
                                    name="post-image"
                                    type="file"
                                    accept="image/*"
                                />
                            </label>
                            {token ? (
                                <input
                                    type="hidden"
                                    name="token"
                                    value={token}
                                />
                            ) : (
                                ''
                            )}
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

function CreateProject() {
    const { token } = useContext(LoginContext)
    return (
        <>
            {addFormCss()}
            <div className="container full-height general-body-background">
                <div className="form-container full-height">
                    <div id="form-one-block">
                        <form
                            className="signup-form"
                            action="/createProject"
                            method="post"
                            encType="multipart/form-data"
                        >
                            <label htmlFor="project-title">
                                Project Title
                                <input
                                    type="text"
                                    id="project-title"
                                    name="project-title"
                                    autoComplete="off"
                                    required
                                    maxLength={80}
                                />
                            </label>
                            {AddDateFields()}
                            <label htmlFor="description">
                                Project Description
                                <input
                                    type="text"
                                    id="description"
                                    name="description"
                                    autoComplete="off"
                                    required
                                    maxLength={320}
                                />
                            </label>
                            <label htmlFor="project-image">
                                Project Profile Photo:
                                <input
                                    id="project-image"
                                    name="project-image"
                                    type="file"
                                    accept="image/*"
                                />
                            </label>
                            {token ? (
                                <input
                                    type="hidden"
                                    name="token"
                                    value={token}
                                />
                            ) : (
                                ''
                            )}
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

function EditProfile() {
    const { token } = useContext(LoginContext)
    return (
        <>
            {addFormCss()}
            <div className="container full-height general-body-background">
                <div className="form-container full-height">
                    <div id="form-one-block">
                        <form
                            className="signup-form"
                            action="/editUser"
                            method="post"
                            encType="multipart/form-data"
                        >
                            <label htmlFor="bio">
                                Project Description
                                <input
                                    type="text"
                                    id="bio"
                                    name="bio"
                                    autoComplete="off"
                                    required
                                    maxLength={160}
                                />
                            </label>
                            {token ? (
                                <input
                                    type="hidden"
                                    name="token"
                                    value={token}
                                />
                            ) : (
                                ''
                            )}
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

const NewPostButton = () => {
    const navigate = useNavigate()

    return (
        <>
            <button
                type="button"
                className="login-button"
                aria-label="Create a new post"
                onClick={() => {navigate('/createPost')}}
            >
                New Post
            </button>
        </>
    )
}

const NewProjectButton = () => {
    const navigate = useNavigate()

    return (
        <>
        <button
            type="button"
            className="login-button"
            aria-label="Create a new project"
            onClick={() => {navigate('/createProject')}}
            style={{ padding: '10px', margin: '10px' }}
        >
            New Project
        </button>
        </>
    )
}

export {
    CreatePost,
    CreateProject,
    EditProfile,
    NewPostButton,
    NewProjectButton,
}
