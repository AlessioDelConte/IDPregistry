## Instantiate the IDP Registry backend

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop)

OR

* [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
  and [Docker Compose](https://docs.docker.com/desktop/install/linux-install/)

### Create a new context for the remote deployment

```bash
docker context create ermes --description "ermes" --docker "host=ssh://<user>@ermes"
```

### Set the new context as default

```bash
docker context use ermes
```

### Volumes

We now need to create two separate volumes for the two different triplestores. The volumes will be used to store the
data of the triplestores. **The volumes will be created on the remote machine** and will be mounted on the containers
on startup.

**GraphDB** volume:

```bash
docker volume create -d local kg-graphdb
```

**Virtuoso** volume:

```bash
docker volume create -d local kg-virtuoso
```

### Use docker-compose to start the containers
This should download the two remote images (graphdb and virtuoso) and start the containers on the remote machine.

Configuration options can be passed to the containers from the docker-compose.yml file.

```bash
docker compose -f docker-compose-kg.yml -p idp-kg up -d
```

#### Show logs

```bash
docker logs -f kg-graphdb    # For a single container
docker compose logs -f docker-compose-kg.yml logs -f # For all containers
```

### Import pre-saved data into the volumes 
If you want to import the pre-saved data into the created volumes, you can use the following commands:

```bash
./docker-volume-snapshot.sh restore /projects/volumes_dump/GraphDB.tar.gz kg-graphdb
```

```bash
./docker-volume-snapshot.sh restore /projects/volumes_dump/Virtuoso.tar.gz kg-virtuoso
```

#### Import to a remote volume without copying the file to the remote machine

```bash
pv <dump>.tar.gz | docker run --rm -v <volume name>:/destination -i busybox tar xzf - -C /destination
```

#### Export from a remote volume without copying the file to the local machine
```bash
docker run --rm -v <volume name>:/dest -i busybox tar -czvf - -C /dest . > <dump>.tar.gz
```

### Import triples into the triplestores

#### GraphDB

* Open the GraphDB Workbench at http://localhost:7201
* Create a new repository, just set the name, the rest leave it as default
* Open the repository and go to the `Import` tab
* Import the triples from the file `./data/*.ttl`
* For each of the `ttl` file, click import and select target graphs `Named graphs`
* Set the name of the graph to `https://idpcentral.org/registry/<name of resource>`
* The name of the resource can be one of `ped`, `mobidb` or `disprot`
* Click `Import`
* Now if you go to the `Explore/Graphs overview` you should see the imported graphs

#### Virtuoso

* Open the Virtuoso interface at http://localhost:8890
* Click on `Conductor`
* Login with the default credentials `dba`/`dba` (password can be changed in the docker-compose.yml file)
* Go to `Linked Data` -> `Quad Store Upload`
* Upload the file `./data/*.ttl`
* For each of the `ttl` file, set the `Named Graph IRI` to `https://idpcentral.org/registry/<name of resource>`
* Click `Upload`
* Now if you go to the `Linked Data` -> `Graphs` -> `Graphs` you should see the imported graphs

### Export volume data as a tar.gz file
```bash
./docker-volume-snapshot.sh create kg-graphdb GraphDB.tar.gz 
```

```bash
./docker-volume-snapshot.sh create kg-virtuoso Virtuoso.tar.gz 
```
