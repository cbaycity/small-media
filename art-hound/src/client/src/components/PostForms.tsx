// A File containing forms for post creation, project creation, and profile creation.

import react, { useState, useContext, useEffect } from 'react'
import { LoginContext } from './LoginForm'

const addFormCss = () => {
    return (
        <>
            <link rel="stylesheet" href="public/basic-form.css" />
        </>
    )
}

const addDateFields = () => {
    const today = new Date().toISOString().split('T')[0] // Format date as yyyy-mm-dd
    return (
        <>
            <label htmlFor="start-date">
                Start Date:
                <input
                    type="date"
                    id="start-date"
                    name="start-date"
                    value={today}
                    required
                />
            </label>
            <label htmlFor="end-date">
                End Date:
                <input
                    type="date"
                    id="end-date"
                    name="end-date"
                    value={today}
                    required
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
        const fetchData = async () => {
            try {
                const response = await fetch('/feed', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token }),
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
                        >
                            <label htmlFor="post-title">
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
                            {addDateFields()}
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
                            <label htmlFor="post-image">
                                Post Photo:
                                <input type="file" accept="image/*" />
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
                        >
                            <label htmlFor="project-title">
                                Project Title
                                <input
                                    type="text"
                                    id="title"
                                    name="title"
                                    autoComplete="off"
                                    required
                                    maxLength={80}
                                />
                            </label>
                            {addDateFields()}
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
                                <input type="file" accept="image/*" />
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

export { CreatePost, CreateProject, EditProfile }
