# Extract data from SQLite - Transform - Load to PostgresSQL

* This is boilerplate for ETL

## Installation && Run
### Git clone
https://github.com/GennadyBr/etl-sqlite-postgres-boilerplate.git


### Create .env file from .env.example
```
cp .env.example .env
```


### Run postgres db in docker
```
docker compose up -d
cd src && python main.py
```

## FastAPI open API
![image1.png](src%2Fimage%2Fimage1.png)

## Features
- FastAPI;
- CRUD for SQLite;
- CRUD for PostgresSQL;
- Postgres in Docker;
- simple extract from SQLite;
- simple load to PostgresSQL;