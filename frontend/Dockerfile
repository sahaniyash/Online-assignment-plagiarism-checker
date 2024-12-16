FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the React app source code
COPY . .

# Expose the port the React app will run on
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
