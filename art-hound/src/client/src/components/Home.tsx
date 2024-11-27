import React, { useContext } from 'react'
import { LoginContext, LoginForm } from './LoginForm'

function Home() {
    const { token } = useContext(LoginContext);

    return (
        <div className="container center-body">
            {!token? <LoginForm /> : <p>Need to build the Home website.</p>}
        </div>
    )
}

export default Home
