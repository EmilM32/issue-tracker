# Build project

```
docker-compose build
```

# Run project
First of all run migrations to db:
```
docker-compose run backend alembic upgrade head
```

to see live logs run
```
docker-compose up
```

or run in background

```
docker-compose up -d
```
