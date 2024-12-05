// A File containing forms for post creation, project creation, and profile creation.

import react, { useState } from 'react'

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
                            <label htmlFor="project">
                                Related Project
                                <input
                                    type="text"
                                    id="project"
                                    name="project"
                                    autoComplete="off"
                                    maxLength={160}
                                />
                            </label>
                            <label htmlFor="post-image">
                                Post Photo:
                                <input type="file" accept="image/*" />
                            </label>
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

function CreateProject() {
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
                                Post Title
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
                            <label htmlFor="profile-image">
                                Profile Photo:
                                <input type="file" accept="image/*" />
                            </label>
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

function EditProfile() {
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

                            <button type="submit">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

export { CreatePost, CreateProject, EditProfile }
