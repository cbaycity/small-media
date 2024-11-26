import react, { createContext, useContext, useState, ReactNode, useEffect } from 'react';

/*
General Idea:
1. Define a variable and setter function that will store/set a login token.
2. Define a function that pings the backend to see if the token is valid, if so, return the token else false.
3. The login page imports the setter function and uses it.
*/

const [userToken, setUserToken] = useState(null);

