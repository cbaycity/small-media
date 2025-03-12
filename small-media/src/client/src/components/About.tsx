import React from 'react'

function About() {
    return (
        <div className="container about-me-body center-body general-body-background full-height">
            <div className="p40">
                <img
                    className="portrait"
                    src="/api/public/BayardPhoto.png"
                    alt="Bayard Carlson, Small Media founder."
                ></img>
            </div>
            <div className="p40 about-me-text div-body">
                <p>
                    Small Media is a place where people can post their art,
                    project updates, and other work in posts that are linked to projects. This hopefully focuses the application on user's work and creative pursuits.
                </p>
                <p>
                Long term goals include ensuring that the platform has discoverability without allowing generative AI models to train on user data.
                </p>
                <p>This website is built by <a href="https://www.linkedin.com/in/charles-carlson-14aa1090/">Charles Bayard Carlson</a> as a project to improve his full stack development skills. The tech stack includes a React front end, a Flask Backend, and a MongoDB database.</p>
            </div>
        </div>
    )
}

export default About
