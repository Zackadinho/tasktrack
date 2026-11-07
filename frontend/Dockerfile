# Multi-stage build: a Node image compiles the app, then a tiny nginx image serves the result.
# The final image has no Node, no source code and no node_modules, just static files.

# ---- Stage 1: build ----
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci                           # like `npm install` but exact versions from the lockfile (use in CI)
COPY . .
# The backend URL is baked into the JavaScript at build time.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build                    # outputs to /app/dist

# ---- Stage 2: serve ----
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
