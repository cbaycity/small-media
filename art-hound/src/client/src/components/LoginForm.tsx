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
const LoginContext = createContext<LoginState| undefined>(undefined)

const LoginProvider: React.FC<{ children: ReactNode }> = ({children}) => {
    
    const [user, setUser] = useState<string | null>(null)
    const [token, setToken] = useState<string | null>(null)

    const storeUser = (newUser: string) => {
        setUser(newUser)
        localStorage.setItem("user", newUser)
    }

    const storeToken = (newToken: string) => {
        setToken(newToken)
        localStorage.setItem("token", newToken)
    }

    const logOut = () => {
        setUser(null)
        localStorage.removeItem('user')
        setToken(null)
        localStorage.removeItem('token')
    }
    return (
        <LoginContext.Provider value={{user, storeUser, token, storeToken, logOut}}>
            {children}
        </LoginContext.Provider>
    )
}

const FormSubmit = async (loginEvent: FormEvent<HTMLFormElement>, loginContext: LoginState) => {
    loginEvent.preventDefault()

    const { user, storeUser, token, storeToken } = loginContext;

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
            if (data.token) {
                storeUser(formData.username)
                storeToken(data.token)
            } else {
                console.error('Failed login. Status: ', response.status)
            }
        } else {
            console.error('Failed Login: Status: ', response.status)
        }
    } catch (error) {
        console.error('Login failed: ', error)
    }
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

const CheckLogin = async (token: string): Promise<boolean> => {
    try {
    const response = await fetch('/validLogin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"token": token}),
    })
    return response.ok
}
    catch (error){
        console.error('Error during user token validation:', error);
        return false
    }
}

export { LoginForm, LoginContext, LoginProvider, CheckLogin}
