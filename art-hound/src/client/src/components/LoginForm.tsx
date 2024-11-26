import react, {
    createContext,
    useContext,
    useState,
    ReactNode,
    useEffect,
    FormEvent,
} from 'react'


interface LoginContextData {
    username: string
    token: string
}

interface LoginFormData{
    username: string // username or email
    password: string // associated password
}


const FormSubmit = async (loginEvent: FormEvent<HTMLFormElement>) => {
    loginEvent.preventDefault();

    const formData: LoginFormData = {
        username: ((loginEvent.target as HTMLFormElement).elements.namedItem("username") as HTMLFormElement)?.value as string,
        password: ((loginEvent.target as HTMLFormElement).elements.namedItem("password") as HTMLFormElement)?.value as string,
    };

    console.log(formData); // print data to see that things are working as expected.

    var loginContext = {"username": "not set", "token": "not set"}

    // Send data to backend to see if login succeeds
    try {
        const response = await fetch("/userLogin",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            const data = await response.json();

            if (data.token) {
                const loginContext = {"username": formData.username, "token": data.token}
            }
            else { 
                console.error("Failed login. Status: ", response.status)
            }
        }
        else{
            console.error("Failed Login: Status: ", response.status)
        }
    }
    catch (error) {
        console.error("Login failed: ", error)
    }
    console.log("LoginContext: ", loginContext)
};

function LoginForm() {
    const [userToken, setUserToken] = useState(null)

    const UserToken = createContext(null)    

    return (
        <div className="container full-height general-body-background">
            <div className="form-container">
                <div id="form-one-block">
                    {/*The below p object displays error messages*/}
                    <form
                        className="signup-form"
                        onSubmit={FormSubmit}
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

export default LoginForm
