# Vue frontend

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

## Docker commands

### Build image

`docker build -t pedrojunqueira/natours-frontend .`

### Run Container

`docker run -it -p 8080:8080 --rm --name natours-vue pedrojunqueira/natours-frontend`

### hack containers

`docker exec -it <mycontainer> /bin/sh`

### build container and run

`docker-compose up --build`

### Shut down containers

`docker-compose down`

### Run app as a microservice

`docker-compose up`
