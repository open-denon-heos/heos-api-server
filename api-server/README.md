# API Server

Objective: API server to query heos telnet interface.
Do not impact original heospy package (only bug fix if needed and fix original repo via PR)

## Local setup

```commandline
pip install -r requirements.txt 
export FLASK_APP=heos_server
flask run
```

## Using Docker in dev mode

```commandline
docker build . -t heos-server
docker run --volume=/home/scoulomb/heospy/api-server/config:/working_dir/api-server/config -p 5000:5000 --name heos-api-server heos-server
# note if you do -p after heoes server it will be use as a flask env
docker rm heos-api-server
docker exec -it heos-api-server /bin/sh

```

## Using Docker compose in dev mode

````commandline
docker-compose up
````

## Deliver docker image

````commandline
docker build . -t scoulomb/heos-api-server:1.0.0
docker login
docker push scoulomb/heos-api-server:1.0.0
````

## Run production image 

````commandline
docker-compose -f PRD.docker-compose.yaml up
````

## Run on QNAP NAS

- Go to `create > search > docker hub > scoulomb/heos-api-server > install`
- Go to `advanced settings` to:
    - `Network` and configure port forwarding `5000:5000` (`host:container`)
    - `Shared folder` and  `Volume from host:Mount Point`, add
        - `/Container/config` (copy before `api-server/config` folder in this folder `/Container/config`)
        - `/working_dir/api-server/config`
- click `create`

Note we can not use compose with QNAP as we have a volume via: Go to `Container station > create > create application`.
See https://github.com/wallabag/docker/issues/164.

It seems we do not have to use host network and can keep nat (in `Network`).

We can open a shell in browser and can see we can target inside container API:
```commandline
python
>>> import urllib.request
>>> contents = urllib.request.urlopen("http://127.0.0.1:5000/player/get_now_playing_media").read()
>>> print(contents)
b'{\n  "heos": {\n    "command": "player/get_now_playing_media",\n    "result": "success",\n    "message": "pid=735067990"\n  },\n  "payload": {\n    
```
And same is also working from another container, which we use for UI (as we can not use compose here)