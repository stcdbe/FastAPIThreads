# FastAPI Threads

___

### Description

The example of an asynchronous web application with combination FastAPI and MongoDB. Used Beanie as ODM to link the app
to the database
![](img/docs.png)
___

### Getting Started

#### Running on Local Machine

+ install dependencies using Poetry

````
$ poetry install --no-root
````

+ configure environment variables in `.env` file
+ start app in virtual environment

````
$ gunicorn -c gunicorn.conf.py asgi:app
````

#### Launch in Docker

+ configure environment variables in `.env` file
+ building the docker image

````
$ docker compose build
````

+ start service

````
$ docker compose up -d
````
____

#### Environment variables

| variables                      | description                               |
|:-------------------------------|:------------------------------------------|
| `DEBUG`                        | debug mode, only allowed 1(True)/0(False) |
| `PORT`                         | app port                                  |
| `JWT_SECRET_KEY`               | a secret key for jwt encoding             |
| `JWT_ALGORITHM`                | jwt encoding algorithm                    |
| `ACCESS_TOKEN_EXPIRES`         | access token lifetime in minutes          |
| `MONGO_HOST`                   | Mongo host                                |
| `MONGO_PORT`                   | Mongo port                                |
| `MONGO_DB`                     | Mongo database                            |
| `MONGO_USER_COLLECTION`        | Mongo user collection                     |
| `MONGO_THREAD_COLLECTION`      | Mongo thread collection                   |
| `MONGO_HOST_TEST`              | Mongo test host                           |
| `MONGO_PORT_TEST`              | Mongo test port                           |
| `MONGO_DB_TEST`                | Mongo test database                       |
| `MONGO_USER_COLLECTION_TEST`   | Mongo test user collection                |
| `MONGO_THREAD_COLLECTION_TEST` | Mongo test thread collection              |

____

#### Tech Stack

+ `FastAPI`
+ `pymongo`, `motor`
+ `gunicorn`
+ `pytest`, `pytest-asyncio` and `httpx` for tests
+ `docker` and `docker-compose`