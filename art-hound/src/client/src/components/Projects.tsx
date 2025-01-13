import React, { useState, useContext, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { LoginContext, CheckLogin } from './LoginForm'
import { LeftBar, RightBar } from './Sidebars'
import { PostData } from './Feed'
import { Link } from 'react-router-dom'

interface Project {
    title: string
    username: string
    startDate: string
    endDate: string
    description: string
    image_id: string | null
    project_id: string
}

interface FullProject {
    title: string
    username: string
    startDate: string
    endDate: string
    description: string
    image_id: string | null
    project_id: string
    posts: PostData[]
}
interface AddPostsForProjectProps {
    postsList: PostData[]
}

const AddPostsForProject: React.FC<AddPostsForProjectProps> = ({
    postsList,
}) => {
    const { token, user } = useContext(LoginContext)
    if (postsList == null) {
        return <></>
    }
    const today = new Date()

    return (
        <>
            <div id="feed" className="feed">
                {postsList && postsList.length > 0 ? (
                    postsList.map((post, index) => (
                        <div className="post" key={index}>
                            <h3>{post['title']}</h3>
                            <p>{post['project']}</p>
                            <p>
                                {post['startDate'] === post['endDate']
                                    ? post['startDate']
                                    : `${post['startDate']} - ${post['endDate']}`}
                            </p>
                            <p>{post['description']}</p>
                            <img
                                className="post-img"
                                src={`/postphotos/${post['image_id']}/${token}`}
                                alt="Photo from post."
                            />
                        </div>
                    ))
                ) : (
                    // No Posts to display
                    <div className="post">
                        <h3 className="post-header">
                            <span>No Posts to Display</span>
                            <span>{user}</span>
                        </h3>
                        <p>
                            {today.toLocaleDateString('en-US', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                            })}
                        </p>
                        <p>
                            This project has no posts, consider creating some
                            and adding them.
                        </p>
                        <img
                            className="post-img"
                            src="/public/artHoundLogoColor.svg"
                            alt="Art Hound Logo"
                        />
                    </div>
                )}
            </div>
            <link rel="stylesheet" href="public/feed.css" />
        </>
    )
}

function DisplayProject(project: Project, token: string | null, index: number) {
    return (
        <div className="project" key={index}>
            <h3>
                <Link
                    to={`/projects/${project['username']}/${project['project_id']}`}
                    className="project-link"
                >
                    {project['title']}
                </Link>
            </h3>
            <p>Owner: {project['username']}</p>
            <p>
                {project['startDate'] === project['endDate']
                    ? project['startDate']
                    : `${project['startDate']} - ${project['endDate']}`}
            </p>
            <p>{project['description']}</p>
            {project['image_id'] && token ? (
                <img
                    className="project-image"
                    src={`/postphotos/${project['image_id']}/${token}`}
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
                    projects. We hope you only see meaningful content that you
                    'subscribe' to!
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
                <div className="container center-body general-body-background space-between">
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

function SingleProject() {
    const { username, project_id } = useParams<{
        username: string
        project_id: string
    }>()

    const [project, setProject] = useState<FullProject>()
    // Create a list of posts which has dictionaries of the post.
    const { token } = useContext(LoginContext)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const projectQuery = async () => {
            try {
                const response = await fetch(
                    `/project/${username}/${project_id}`,
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ token: token }),
                    }
                )

                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`)
                }

                const data = await response.json()
                setProject(data)
            } catch (err: any) {
                setError(err.message || 'An error occurred.')
            }
        }
        projectQuery()
    }, [token])

    if (error) {
        return <div>Error: {error}</div>
    }

    if (project)
        return (
            <>
                <div>
                    <h3>{project['title']}</h3>
                    <p>Owner: {project['username']}</p>
                    <p>Description: {project['description']}</p>
                </div>
                <div>
                    {project['image_id'] && token ? (
                        <img
                            className="project-image"
                            src={`/postphotos/${project['image_id']}/${token}`}
                            alt="Main project photo."
                        />
                    ) : (
                        <></>
                    )}
                    <h3>Activity:</h3>
                    <AddPostsForProject postsList={project['posts']} />
                </div>
            </>
        )
    return <></>
}

export { Projects, SingleProject }

/*
To solve the issue where project titles cannot be used in links, maybe link using project id?
Questions:
1. Do the ids have URL safe characters and format? Yes.
2. Do you need to change the backend functions to search for project ID? Yes.
3. Do you need to change the front end interfaces to accept project id? Yes.
4. Should you use project ID or database id? project_id
*/
