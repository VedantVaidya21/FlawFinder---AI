# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++ libc6-compat

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Install regular React plugin as alternative to SWC
RUN npm install @vitejs/plugin-react

# Copy source code
COPY . .

# Copy Docker-specific Vite config
COPY vite.config.docker.js ./

# Build the application using Docker config
RUN npm run build -- --config vite.config.docker.js

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Install serve globally
RUN npm install -g serve

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "dist", "-l", "3000"]
