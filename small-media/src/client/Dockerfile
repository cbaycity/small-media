FROM node:22.8.0

# Create app directory
WORKDIR /client

# Copy source files to the needed directory
COPY . .

# Install app dependencies
RUN npm install

# Expose the port your app listens on
EXPOSE 3000

# Start the app
CMD [ "npm", "start" ]
