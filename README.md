# NGINX_SSO_DOCKER
proof of concept - OpenDJ+OpenAM+NGINX with modAM+MongoDB+ flask app :: base on Docker deploy


## Purpose

NGINX_SSO_DOCKER is proof of concept deploy solution.


For testing, to solution was added  microservices written on python flask.
The Flask application have 2 endpoints:
- The first endpoint accept only POST requests which have a json payload.
The endpoint store the data in a mongo data store.
- The second endpoint accept GET requests with an uid parameter, date parameter and will return the
number of occurrences of a given UID  for that day.


####Project consist:
```
OpenDJ              - Dockerfile.opendj
OpenAM              - Dockerfile.openam
MongoDB             - Dockerfile.mongodb
Nginx with modAM    - Dockerfile.nginxmodam
python microservice - Dockerfile.pymicroservice  
```


## Deploy Docker container with ForgeRock OpenDJ

This repository contains Dockerfile and resources to build a Docker image with ForgeRock version OpenDJ 4.0.0-20160505.
Please see `opendj-install.properties` for default cn and password (see below, Build Notes, for other info).

## Usage

#### How to deploy and run
```
1. git clone git@github.com:andriipetruk/forgerock-docker.git
2. cd forgerock-docker
3. docker build -t opendj -f Dockerfile.opendj .
4. docker run  -d -p 1389:1389 -p 1636:1636 -p 4444:4444 --name opendj opendj
```

#### Access 
```
ldap://_dockerip_:1389
For [boot2docker](https://docs.docker.com/installation/mac/) users, ldap://_boot2dockerip_:1389
```

### Build Notes

 `opendj-install.properties`
* sets root user DN, password, ports
* installs Example.ldif so there's data; one can comment out `ldifFile` property to build an empty LDAP


## Deploy Docker container with ForgeRock OpenAM

This repository contains Dockerfile and resources to build a Docker image with ForgeRock version OpenAM VERS!!.
Please see `opendj-install.properties` for default cn and password (see below, Build Notes, for other info).

## Usage

#### How to deploy and run
```
1. git clone git@github.com:andriipetruk/forgerock-docker.git
2. cd forgerock-docker
3. docker build -t openam -f Dockerfile.openam .
4. docker run -e KEYSTORE_PASS=secret -v $PWD/config:/root -v $PWD/server.keystore:/opt/server.keystore -v /dev/urandom:/dev/random --name openam --link opendj -p 8443:8443 -p 8080:8080 -d openam
```



#### Access 
```
https://_dockerip_:8443/openam
ldap://_dockerip_:1389
For [boot2docker](https://docs.docker.com/installation/mac/) users, ldap://_boot2dockerip_:1389
```


## Deploy Docker container with MongoDB

## Usage

#### How to deploy and run
```
1. git clone git@github.com:andriipetruk/forgerock-docker.git
2. cd forgerock-docker
3. docker build -t mongodb -f Dockerfile.mongodb .
4. docker run  -v /srv/docker/mongodb:/var/lib/mongodb --name mongo_instance_001 -d --restart=always mongodb  
```


## Deploy Docker container with Flask app 

## Usage

#### How to deploy and run
```
1. git clone git@github.com:andriipetruk/forgerock-docker.git
2. cd forgerock-docker
3. docker build -t pymicroservice -f Dockerfile.pymicroservice .
4. docker run -d  --link mongo_instance_001 --name pymicroservice-inst1 pymicroservice 
```


## Deploy Docker container with Nginx 1.7.7 with mod  OpenAM

## Usage

#### How to deploy and run
```
1. git clone git@github.com:andriipetruk/forgerock-docker.git
2. cd forgerock-docker
3. docker build -t nginxmodam -f Dockerfile.nginxmodam .
4. docker run --link openam  --link pymicroservice-inst1 --add-host="openam.fcloud.io:13.94.159.205" --add-host="www.fcloud.io:13.94.159.205" --name nginxmodam -p 80:8080  -d nginxmodam 
```


#### Access 
```

1. curl -H "Content-Type: application/json" -X POST -d '{"uid": "2", "name": "Jane Doe", "date": "2015-05-13T14:36:00.451765", "md5checksum": "0cf6399e2739304b73b41162735679fb"}' http://_dockerip_:80/api/

2. http://_dockerip_:80/api/2/2015-05-13/

```


