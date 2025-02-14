import react, {
    createContext,
    useState,
    useContext,
    FormEvent,
    useEffect,
    ReactNode,
} from 'react'

interface LoginFormData {
    username: string // username or email
    password: string // associated password
}

// Define the type for the login state
interface LoginState {
    user: string | null
    storeUser: (newUser: string) => void
    token: string | null
    storeToken: (newToken: string) => void
    logOut: () => void
}

// Creates the LoginContext
const LoginContext = createContext<LoginState>({
    user: '',
    storeUser: () => {},
    token: '',
    storeToken: () => {},
    logOut: () => {},
})

const LoginProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<string | null>(null)
    const [token, setToken] = useState<string | null>(null)

    const storeUser = (newUser: string) => {
        setUser(newUser)
        localStorage.setItem('user', newUser)
    }

    const storeToken = (newToken: string) => {
        setToken(newToken)
        localStorage.setItem('token', newToken)
    }

    const logOut = () => {
        setUser(null)
        localStorage.removeItem('user')
        setToken(null)
        localStorage.removeItem('token')
    }

    // Function to set login to the loginState stored if it is stored.
    const StoredLoginDetails = () => {
        var user = localStorage.getItem('user')
        var token = localStorage.getItem('token')
        if (user != '' && user != null) {
            setUser(user)
        }
        if (token != '' && token != null) {
            setToken(token)
        }
    }

    // Set user and token if they're stored.
    useEffect(() => {
        StoredLoginDetails()
    }, [])

    return (
        <LoginContext.Provider
            value={{ user, storeUser, token, storeToken, logOut }}
        >
            {children}
        </LoginContext.Provider>
    )
}

const FormSubmit = async (
    loginEvent: FormEvent<HTMLFormElement>,
    loginContext: LoginState,
    incorrectLoginSetter: react.Dispatch<react.SetStateAction<boolean>>
) => {
    loginEvent.preventDefault()

    const { user, storeUser, token, storeToken } = loginContext

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
        const response = await fetch('/api/userLogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })

        if (response.ok) {
            const data = await response.json()
            if (data.token) {
                storeUser(data.username)
                storeToken(data.token)
            } else {
                console.error('Failed login. Status: ', response.status)
            }
        } else {
            incorrectLoginSetter(true) // Set invalid login to true.
            console.error('Failed Login: Status: ', response.status)
        }
    } catch (error) {
        console.error('Login failed: ', error)
    }
}

function LoginForm() {
    const loginContext = useContext(LoginContext)

    if (!loginContext) {
        throw new Error('LoginForm must be used within a LoginProvider')
    }

    const [invalidLogin, setInvalidLogin] = useState(false)

    return (
        <div className="full-height general-body-background">
            <div className="form-container">
                <div id="form-one-block">
                    <form
                        className="signup-form"
                        onSubmit={(e) =>
                            FormSubmit(e, loginContext, setInvalidLogin)
                        }
                        method="post"
                    >
                        <h2>Signin</h2>
                        {invalidLogin ? (
                            <h3>
                                Login failed due to invalid credentials. Please
                                try again.
                                <br />
                            </h3>
                        ) : null}
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
                <link rel="stylesheet" href="/api/public/basic-form.css" />
            </div>
        </div>
    )
}

const CheckLogin = async (token: string | null): Promise<boolean> => {
    try {
        const response = await fetch('/api/validLogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: token }),
        })
        return response.ok
    } catch (error) {
        console.error('Error during user token validation:', error)
        return false
    }
}

export { LoginForm, LoginContext, LoginProvider, CheckLogin }
