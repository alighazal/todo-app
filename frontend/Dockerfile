FROM node:22-alpine

WORKDIR /app

# Install dependencies separately for better Docker layer caching
COPY package*.json ./
RUN npm install

# Copy the rest of the app source
COPY . .

EXPOSE 3000

# Run the Vite dev server in the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

