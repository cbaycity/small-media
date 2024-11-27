### Development Notes:

1. The backend is Flask, the front end is react. Flask needs to server all files from assets whenever requested, without authentication. This is because these files are just CSS and formatting Javascript.
2. The React components displying content need to make requests for this content to the backend, which will check authentication.

The react front end was built with `npx create-react-app client --template typescript`. By adding a `proxy` to `package.json`, the front end is connected to the backend. By connect, I mean that when react requests a file using a relative path, it will prepend the proxy to get the end path.

## Useful commands:

1. The command `flask --app main run` can be from from the backend directory to start up a development server. You need the poetry environment to be runnning and setup correctly.
2. The front end can be started by running `npm start` in the client directory.
   Note: Once this is done, you can see that the app is delivered by the NPM server but it is requesting reasources from the Flask server. This will let us build an Apache Kafka backend database management via Flask but we'll focus on building the front end web experience using the NPM app. These two components are connected with proxy variable in the react app, which directs the traffic to the Flask server.
3. `docker compose up --build` will start all of the services. `docker compose --profile explore up --build` will start the jupyter notebook too that can explore the database.
4. Need to create Python requirements file
```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

## Current to do:

1. Add a Create Post button to replace the login button in the header.
2. Add a projects section (Notably, let artists add each other to a project.)
3. Add a friends page and following projects.
4. Manage logins session.

Future to do:
1. Store hashed passwords (Done!)
2. Protect against Request Forgery.
3. Enable username or email based login.

## Mac Environment Setup:

1. Use brew to install Python
2. install 3.12.3
3. create a python environment off of 3.12.3
4. pip install poetry
5. use poetry shell for development
6. Set default vscode interpreter to the poetry shell env.
7. Had to turn off airplay reciever to open up port 5000 for development with Docker.

## Linter Notes:

```bash
python -m black <target>
prettier <target: ex. ./*> --write
```


### Sample Users:
username: test
password: Password1
