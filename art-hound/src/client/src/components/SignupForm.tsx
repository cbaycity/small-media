import React from 'react';
import { useRef, useState, useEffect} from 'react';


const USER_VALIDATION = /^[a-zA-Z][a-zA-Z0-9-_]{3,20}$/
const PASSWORD_VALIDATION = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/


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

    const [ errMsg, setErrMsg ] = useState('');
    const [ success, setSuccess ] = useState(false);

    /* Checks if the user's screen is focused on the current component.*/
    useEffect(() => {
        if (userRef.current){
            userRef.current.focus();
        }
    }, [])

    /* The arrays at the end are dependencies for the function to run. The function above has no deps while the one below runs when user is set.*/

    useEffect(() => {
        const result = USER_VALIDATION.test(user);
        console.log(result);
        console.log(user);
        setValidName(result);
    }, [user])


    /* Once both the pwd and matchPwd are set, check that the values match and are valid.*/
    useEffect(() => {
        const result = PASSWORD_VALIDATION.test(pwd);
        console.log(result);
        console.log(pwd);
        setValidPwd(result);
        const match = pwd === matchPwd;
        setValidMatch(match);
    }, [pwd, matchPwd])

    /* Clear the error message if the user tries to set a new username, pwd, or matchpwd. */
    useEffect(() => {
        setErrMsg("");
    }, [user, pwd, matchPwd])

    return (
        <div className="container">
            <></>
            <section>
                {/*The below p object displays error messages*/}
                <p ref={errRef} className={ errMsg ? "errMsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
                <h1>Signup</h1>
                <form action="/createAccount" method="post">
                    <p>Username:<input
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
                        maxLength={30}/></p>
                    <p id="uidnote" className={userFocus && user && !validName ? "instructions": "offscreen"}>
                        4 to 24 characters.<br />
                        Must begin with a letter.<br />
                        Only letters, numbers, underscores, hyphens allowed.
                    </p>
                    <p>Email:<input type="email" name="email"/></p>
                    <p>Password:<input type="password" name="password" maxLength={30}/></p>
                    <p>Confirm Password:<input type="password" name="_" maxLength={30}/></p>
                    <p>Submit<input type="submit" value="Submit"></input></p>
                </form>
                {/*Add the stylesheet to the CSS.*/}
                <link rel="stylesheet" href="public/signup-form.css" />
            </section>
        </div>
    );
};

function ProfileCreation() {
    return <p>In Development.</p>
};

export {AccountCreation, ProfileCreation};