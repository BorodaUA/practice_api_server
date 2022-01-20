## practice API Server
A pet project API to get familiar with flask.  
This repository is a part of [practice_flask](https://github.com/BorodaUA/practice_flask.git) project.
## Install & run
### How to use docker commands to run this Dockerfile:
1. Create Docker image for the project
```
docker build -t ${PWD##*/}-image .
```
2. Run project's Docker container
```
docker run -d -p 4800:4800 -v ${PWD}:/usr/src/app --name ${PWD##*/}-container ${PWD##*/}-image
```
3. Stop and remove project's Docker container
```
docker rm -f ${PWD##*/}-container
```
4. Remove project's Docker image
```
docker image rm -f ${PWD##*/}-image
```
