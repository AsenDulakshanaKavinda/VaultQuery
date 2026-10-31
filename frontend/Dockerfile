# 1. build he vite react app
FROM node:24-alpine AS builder

WORKDIR /app

# Copy dependency manifests and install dependencies (cached layers)
COPY package*.json ./
RUN npm ci

# Copy the rest of the application source code
COPY . .

# Build the app (outputs static files to /app/dist)
RUN npm run build

# 2. Serve app with Nginx
FROM nginx:alpine as production

# Copy built static assets from the builder stage into Nginx's web root
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 to traffic
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
