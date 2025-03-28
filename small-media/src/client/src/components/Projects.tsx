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
                            <p>
                                <Link
                                    to={`/projects/${post['username']}/${post['project_id']}`}
                                    className="project-link"
                                >
                                    {post['title']}
                                </Link>
                            </p>
                            <p>
                                {post['startDate'] === post['endDate']
                                    ? post['startDate']
                                    : `${post['startDate']} - ${post['endDate']}`}
                            </p>
                            <p>{post['description']}</p>
                            <img
                                className="post-img"
                                src={`/api/postphotos/${post['image_id']}`}
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
                            src="/api/public/artHoundLogoColor.svg"
                            alt="Art Hound Logo"
                        />
                    </div>
                )}
            </div>
            <link
                rel="stylesheet"
                href={`/${process.env.PUBLIC_URL}/api/public/feed.css`}
            />
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
                {project['startDate'] === project['endDate'] ||
                project['endDate'] == null
                    ? `Started: ${project['startDate']}`
                    : `Dates: ${project['startDate']} - ${project['endDate']}`}
            </p>
            <p>{project['description']}</p>
            {project['image_id'] && token ? (
                <img
                    className="project-image"
                    src={`/api/postphotos/${project['image_id']}`}
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
        <div id="feed" className="feed max-width">
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
    const [friendsProjects, setFriendsProjects] = useState<Project[]>([])
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
                const response = await fetch(`/api/UserProjects`, {
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

    // Gets a User's Friend's projects list.
    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await fetch(`/api/FriendProjects`, {
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
                setFriendsProjects(data)
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
            <link
                rel="stylesheet"
                href={`/${process.env.PUBLIC_URL}/api/public/feed.css`}
            />
            <div className="center-body general-body-background feed-body">
                <LeftBar />
                <div className="container center-body general-body-background space-between basic-padding">
                    <div className="userProjects">
                        <h2>Your Projects:</h2>
                        <div>
                            {DisplayListProjects(userProjects, token)}
                        </div>
                    </div>
                    <div className="userProjects">
                        <h2>Friend's Projects:</h2>
                        <div>
                            {DisplayListProjects(friendsProjects, token)}
                        </div>
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
                    `/api/project/${username}/${project_id}`,
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
            <div className="center-body general-body-background feed-body">
                <div className="side-bar left-bar-projects">
                    <div>
                        <h3>{project['title']}</h3>
                        <p>Owner: {project['username']}</p>
                        <p>Description: {project['description']}</p>
                    </div>
                    <div>
                        {project['image_id'] && token ? (
                            <img
                                className="project-image"
                                src={`/api/postphotos/${project['image_id']}`}
                                alt="Main project photo."
                            />
                        ) : (
                            <></>
                        )}
                    </div>
                </div>
                <div id="feed" className="feed">
                    <h3>Activity:</h3>
                    <AddPostsForProject postsList={project['posts']} />
                </div>
                <RightBar />
            </div>
        )
    return <></>
}

export { Projects, SingleProject }
