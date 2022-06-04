# API Server

Objective: API server to query HEOS telnet interface.
It leverages https://github.com/open-denon-heos/heospy.

## Local setup

```commandline
pip install -r requirements.txt 
export FLASK_APP=heos_server
flask run
```

## Using Docker in dev mode

```commandline
docker build . -t heos-server
docker run --volume=/home/scoulomb/heospy/api-server/config:/working_dir/api-server/config --network host --name heos-api-server heos-server
# note if you do -p after heoes server it will be use as a flask env
docker rm heos-api-server
docker exec -it heos-api-server /bin/sh

```

- Note we do not do port forwarding `-p 5000:5000` because we use `host` network. Host networks allows to 
  - perform service discovery
  - get node local IP in `index.html`

- We perform a volume mapping with the folder containing the config file: `/home/scoulomb/heospy/api-server/config:/working_dir/api-server/config`
Here is a sample config [file](./config/config.json).

Alternative to config file is to use environment variable.
- CONF_PLAYER_NAME
- CONF_USER
- CONF_PW 

When used, at start up server will create following config file

```json
{
  "player_name": "Denon AVR-X2700H",
  "user": "fake@gmail.com",
  "pw": "do-not-use-qwerty-as-your-password"
}
```

This is convenient in environment where volume mapping is not possible (for [example QNAP](#run-on-qnap-nas) when used with Docker compose does not support volume)
However volume mapping avoid a new discovery at every container restart.
It can be used in combination ith volume but it will overwrite the config file.

## Using Docker compose in dev mode

See [docker compose](../docker-compose.yaml).


````commandline
docker-compose up --build
````


## Deliver docker image

````commandline
docker build . -t scoulomb/heos-api-server:1.0.0
docker login
docker push scoulomb/heos-api-server:1.0.0
````

## Run production image 

See [docker compose](../PRD.docker-compose.yaml).

````commandline
docker-compose -f PRD.docker-compose.yaml up
````


## Run on QNAP NAS

### With volume mapping

Note we can not use compose with QNAP as we have a volume via: Go to `Container station`.
See https://github.com/wallabag/docker/issues/164.

- Go to `create > search > docker hub > scoulomb/heos-api-server > install`
- Go to `advanced settings` to:
    - `Network` and either 
      - configure port forwarding `5000:5000` (`host:container`) -> service discovery will not work, so config file should contain a full configuration
      - use host network 
    - `Shared folder` and  `Volume from host:Mount Point`, add
        - `/Container/config` (copy before `api-server/config` folder in this folder `/Container/config`)
        - `/working_dir/api-server/config`
- click `create`

Rather than using container station UI could do:

```commandline
docker run --volume=/Container/config:/working_dir/api-server/config -p 5000:5000 --name heos-api-server scoulomb/heos-api-server:1.0.0
```


### Without volume mapping

We will leverage environment var.

Go to `Container station > create > create application`.

Copy [docker compose YAML file](../PRD.docker-compose.yaml).

Be sure to delete existing container and then image when pushing same tag.

If error to del image via container station use ssh (this is needed when pushed same tag)
```commandline
docker image rm 981e8a99b878 118c43dad86a d52a5eb4997e 17f3a401dac2 --force
```

## Prepare for client (UI)

UI can be in compose file (will create a network) but can also use (with port mapping or host network) loopback ip

We can open a shell in browser from another container and can do

```commandline
python
>>> import urllib.request
>>> contents = urllib.request.urlopen("http://127.0.0.1:5000/player/get_now_playing_media").read()
>>> print(contents)
b'{\n  "heos": {\n    "command": "player/get_now_playing_media",\n    "result": "success",\n    "message": "pid=735067990"\n  },\n  "payload": {\n    
```


<!--

We can define `local.nas.coulombel.net` as A record to NAS local IP.
index.html will now point node ip due to improvement made via {{local_ip}} in templates/index.html

-->

