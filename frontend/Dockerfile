# build stage
FROM node:12.16.2-alpine as build-stage
WORKDIR /app

COPY frontend/ .

RUN npm install
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
