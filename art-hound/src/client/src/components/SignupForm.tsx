import React from 'react';
import { useRef, useState, useEffect} from 'react';


const USER_VALIDATION = /^[a-zA-Z][a-zA-Z0-9-_]{3,20}$/
const PASSWORD_VALIDATION = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,20}$/
const EMAIL_VALIDATION = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/

function AccountCreation() {

    const userRef = useRef<HTMLInputElement>(null);
    const errRef = useRef<HTMLInputElement>(null);

    const [ user, setUser ] = useState("");
    const [ validName, setValidName ] = useState(false);
    const [ userFocus, setUserFocus ] = useState(false);

    const [ pwd, setPwd ] = useState("");
    const [ validPwd, setValidPwd ] = useState(false);
    const [ pwdFocus, setPwdFocus ] = useState(false);

    const [ matchPwd, setMatchPwd ] = useState("");
    const [ validMatch, setValidMatch ] = useState(false);
    const [ matchFocus, setMatchFocus ] = useState(false);

    const [ email, setEmail ] = useState("");
    const [ validEmail, setValidEmail ] = useState(false);
    const [ emailFocus, setEmailFocus ] = useState(false);

    const [ errMsg, setErrMsg ] = useState('');
    const [ success, setSuccess ] = useState(false);

    /* Checks if the user's screen is focused on the user component.*/
    useEffect(() => {
        if (userRef.current){
            userRef.current.focus();
        }
    }, [])

    // The arrays at the end are dependencies for the function to run. The function above has no deps while the one below runs when user is set.

    // Checks the username vs the conditions.
    useEffect(() => {
        const result = USER_VALIDATION.test(user);
        console.log("Valid Username: " + result);
        setValidName(result);
    }, [user])

    // Once both the pwd and matchPwd are set, check that the values match and are valid.
    useEffect(() => {
        const result = PASSWORD_VALIDATION.test(pwd);
        console.log("Valid password: " + result);
        setValidPwd(result);
        const match = pwd === matchPwd;
        setValidMatch(match);
    }, [pwd, matchPwd])
    
    // Checks the email vs the conditions.
    useEffect(() => {
        const result = EMAIL_VALIDATION.test(email);
        console.log("Valid email: " + result);
        setValidEmail(result);
    }, [email])

    /* Clear the error message if the user tries to set a new username, pwd, or matchpwd. */
    useEffect(() => {
        if (validName ===false){
            setErrMsg("Usernames must start with a letter, be 3 to 20 characters long, and only contain letters, numbers, and ('-', '_') characters.");
        }
        else if (validPwd === false){
            setErrMsg("Passwords must be at least 8 characters long and contain a number.")
        }
        else if (validMatch === false){
            setErrMsg("Passwords must match.")
        }
        else if (validEmail === false){
            setErrMsg("Please enter a valid email.")
        }
        else {
        setErrMsg("");
        }
    }, [user, pwd, matchPwd, email])

    return (
        <div className="container full-height general-body-background">
            <div className="form-container full-height">
                <div id="form-one-block">
                {/*The below p object displays error messages*/}
                <form className = "signup-form" action="/createAccount" method="post">
                    <h2>Signup</h2>
                    <label htmlFor="username">Username:<input
                        type="text"
                        id = "username"
                        name="username"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(e) => setUser(e.target.value)}
                        required
                        aria-invalid={ validName ? "false" : "true"}
                        aria-describedby='uidnote'
                        onFocus={() => setUserFocus(true)}
                        onBlur={() => setUserFocus(false)}
                        maxLength={30}/></label>
                    <p id="uidnote" className={userFocus && user && !validName ? "instructions": "offscreen"}>
                        4 to 24 characters.<br />
                        Must begin with a letter.<br />
                        Only letters, numbers, underscores, hyphens allowed.
                    </p>
                    <br/>
                    <label htmlFor="email">Email:<input
                        type="text"
                        id = "email"
                        name="email"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        aria-invalid={ validName ? "false" : "true"}
                        aria-describedby='uidnote'
                        onFocus={() => setEmailFocus(true)}
                        onBlur={() => setEmailFocus(false)}/></label>
                    <p id="uidnote" className={emailFocus && email && !validEmail ? "instructions" : "offscreen"}>Enter a valid email address.</p>
                    <label htmlFor="password">Password:<input
                        type="password"
                        id = "password"
                        name="password"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(e) => setPwd(e.target.value)}
                        required
                        aria-invalid={ validName ? "false" : "true"}
                        aria-describedby='uidnote'
                        onFocus={() => setPwdFocus(true)}
                        onBlur={() => setPwdFocus(false)}/></label>
                    <p id="uidnote" className={pwdFocus && pwd && !validPwd ? "instructions": "offscreen"}>
                        9 to 24 characters and it must include a letter and a number.
                    </p>
                    <br/>
                    <label htmlFor="password">Password Match:<input
                        type="password"
                        id = "Matchpassword"
                        name="Matchpassword"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(e) => setMatchPwd(e.target.value)}
                        required
                        aria-invalid={ validName ? "false" : "true"}
                        aria-describedby='uidnote'
                        onFocus={() => setMatchFocus(true)}
                        onBlur={() => setMatchFocus(false)}/></label>
                    <p id="uidnote" className={matchFocus && matchPwd && !validMatch ? "instructions": "offscreen"}>
                        Passwords must match.
                    </p>
                    <br/>
                    <button type="submit">Sign Up</button>
                </form>
                </div>
                {/* Add the stylesheet to the CSS.*/}
                <link rel="stylesheet" href="public/signup-form.css" />
            </div>
        </div>
    );
};

function ProfileCreation() {
    return <p>In Development.</p>
};

export {AccountCreation, ProfileCreation};