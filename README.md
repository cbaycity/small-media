### Development Notes:

1. The backend is Flask, the front end is react. Flask needs to server all files from assets whenever requested, without authentication. This is because these files are just CSS and formatting Javascript.
2. The React components displying content need to make requests for this content to the backend, which will check authentication.

The react front end was built with `npx create-react-app client --template typescript`. By adding a `proxy` to `package.json`, the front end is connected to the backend. By connect, I mean that when react requests a file using a relative path, it will prepend the proxy to get the end path. 

## Useful commands:
1. The command `flask --app main run` can be from from the backend directory to start up a development server. You need the poetry environment to be runnning and setup correctly.
2. The front end can be started by running `npm start` in the client directory.
Note: Once this is done, you can see that the app is delivered by the NPM server but it is requesting reasources from the Flask server. This will let us build an Apache Kafka backend database management via Flask but we'll focus on building the front end web experience using the NPM app. These two components are connected with proxy variable in the react app, which directs the traffic to the Flask server.

## Current to do:

1. Make small icon for logo. Make logo without color. (Done!)
2. Finish Header
  i. Update to new logo and then be done with this component. (Done!)
  ii. Figure out why the centering of the list is changing for some pages. Everything needs to be centered. (Done!)
3. Add images and info to the backend for a single post.  (Done!)
4. Create a signup form. 
  i. Need to control state using Javascript. The userFocus variables need to be updated as does the error checking.
5. Create a database that manages a backend with access.
6. Create the Local Art and Popular Art sections from the general feed components.
7. Figure out some form of testing for the components and for the site. Jack suggests that only testing for backend hits is needed?


## Mac Environment Setup:
1. Use brew to install Python
2. install 3.12.3
3. create a python environment off of 3.12.3
4. pip install poetry
5. use poetry shell for development
6. Set default vscode interpreter to the poetry shell env.
