import react, {
    createContext,
    useState,
    useContext,
    FormEvent,
} from 'react'

interface LoginFormData {
    username: string // username or email
    password: string // associated password
}

// Define the type for the login state
interface LoginState {
    user: string
    setUser: React.Dispatch<React.SetStateAction<string>>
    token: string
    setToken: React.Dispatch<React.SetStateAction<string>>
}

const useLoginState = () => {
    const [user, setUser] = useState('')
    const [token, setToken] = useState('')
    return { user, setUser, token, setToken }
}

const initialLoginState : LoginState = {
    user: "",
    setUser: () => {}, // Placeholder function
    token: "",
    setToken: () => {}, // Placeholder function.
}

// Creates the LoginContext
const LoginContext = createContext<LoginState>(initialLoginState)

const FormSubmit = async (loginEvent: FormEvent<HTMLFormElement>, loginContext: LoginState) => {
    loginEvent.preventDefault()

    const { user, setUser, token, setToken } = loginContext;

    if (!loginContext) {
        console.error('FormSubmit must be used within a LoginContextProvider')
        return
    }

    const formData: LoginFormData = {
        username: (
            (loginEvent.target as HTMLFormElement).elements.namedItem(
                'username'
            ) as HTMLFormElement
        )?.value as string,
        password: (
            (loginEvent.target as HTMLFormElement).elements.namedItem(
                'password'
            ) as HTMLFormElement
        )?.value as string,
    }

    // Send data to backend to see if login succeeds
    try {
        const response = await fetch('/userLogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })

        if (response.ok) {
            const data = await response.json()
            console.log('data.token = ' + data.token)
            if (data.token) {
                setUser(formData.username)
                setToken(data.token)
            } else {
                console.error('Failed login. Status: ', response.status)
            }
        } else {
            console.error('Failed Login: Status: ', response.status)
        }
    } catch (error) {
        console.error('Login failed: ', error)
    }
    console.log('User: ', user, ' Token: ', token)
}

function LoginForm() {
    const loginContext = useContext(LoginContext);

    if (!loginContext) {
        throw new Error('LoginForm must be used within a LoginProvider');
    }

    return (
        <div className="container full-height general-body-background">
            <div className="form-container">
                <div id="form-one-block">
                    {/*The below p object displays error messages*/}
                    <form
                        className="signup-form"
                        onSubmit={(e) => FormSubmit(e, loginContext)}
                        method="post"
                    >
                        <h2>Signin</h2>
                        <label htmlFor="username">
                            Username or Email:
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

function CheckLogin() {
    // Check token with backend...
    return false
}

export { LoginForm, LoginContext, useLoginState}
