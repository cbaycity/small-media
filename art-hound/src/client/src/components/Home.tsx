import React from 'react'

function Home() {
    return (
        <div className="container center-body">
            <p>Need to build the Home website.</p>
        </div>
    )
}

function Login() {
    return (
        <div className="container full-height general-body-background">
            <div className="form-container">
                <div id="form-one-block">
                    {/*The below p object displays error messages*/}
                    <form
                        className="signup-form"
                        action="/createAccount"
                        method="post"
                    >
                        <h2>Signin</h2>
                        <label htmlFor="username">
                            Username:
                            <input
                                type="text"
                                id="username"
                                name="username"
                                required
                            />
                        </label>
                        <label htmlFor="password">
                            Password:
                            <input
                                type="password"
                                id="password"
                                name="password"
                                maxLength={30}
                            />
                        </label>
                        <button type="submit">Login</button>
                    </form>
                </div>
                {/* Add the stylesheet to the CSS.*/}
                <link rel="stylesheet" href="public/signup-form.css" />
            </div>
        </div>
    )
}

export { Home, Login }
