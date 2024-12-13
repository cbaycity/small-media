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

# To Do Lists:
## Priority:
For multiple pages, a common feature needed is a way to retrieve lists of posts to display. You therefore need to spend time creating a "feed" frontend function that returns a list of posts and related details. This function can be called by other elements and queries can be passed to the backend to retrieve posts.

## Infrastructure:
1. You can add tests for routing of the main.py file. You should add these just after launching.
2. Protect against Request Forgery.
3. Add an invite token to the signup page.
4. The login logic isn't working well. When a user signs out they need to stop seeing webpage content. 

## Projects: 
1. Show projects in a list that the user has.
2. Have a way to click into projects and see posts displayed.

## Profile Section:
1. Split profile page into two sections: activities, and projects.
2. Add edit profile button.

## Friends Section:
1. Let artists add each other to a project.
2. Let artists add each other as friends and see each other's accounts.


# Mac Environment Setup:

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


### Deploy to AWS using AWS ECR Repository
1. Place to push and store Docker images.
2. Use EC2 instance to just trigger ```docker run```.
3. Put a firewall, like AWS waff, to stop bots.

