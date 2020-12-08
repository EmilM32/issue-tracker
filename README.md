# Build project

To build project
```
docker-compose build
```

After first build you need to create migrations to database.

Run containers at background running and enter backend container
```
docker-compose up -d
```
```
docker-compose exec backend bash
```

Inside container create init migrations
```
alembic revision --autogenerate -m 'Init'
```
and update head
```
alembic upgrade head
```

If you don't need any migrations you can run
```
docker-compose up
```
to see live logs.