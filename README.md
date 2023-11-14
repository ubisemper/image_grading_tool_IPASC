

## SIMPA PAI label toolkit

This is a 'simple' labaling toolkit to label PAI generated images. Due to the fact that the implementation is still unkown, the backend is a bit more complex to deal with further requirements more easily

## How it works and how to run locally
The toolkit is broken down in 4 parts
- [Nextjs13](https://nextjs.org/blog/next-13) for frontend 
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) for backend API 
- [S3 ninja](https://s3ninja.net/) storage emulator
- [Reddis](https://hub.docker.com/_/redis) for task management

First setup the backend services:
- Start s3 storage emulator: `docker run -p 9444:9000 scireum/s3-ninja`
- Start reddis storage: `docker run -p 6379:6379 --name some-redis -d redis`

To run the celery task manager and flask api navigate to the `/api/` folder in the main project.
-  Start Flask api: `python3 -m flask --app api/index run -p 5328`
-  Start Celery service: `celery -A index.celery worker --loglevel=info `

Then to start the frontent, be in the root of the project and run: `yarn run next-dev`

Then a connection can be made to `localhost:3000/dashboard`

## How to use the toolkit
TODO

## Local Deployment
All the dockers have to be tied together in a docker compose, the flask & storage emulator are already fixed, but now the rest of the services.

## Web deployment
TODO

