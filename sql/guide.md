**How to install Postgresql in docker**
`docker run --name postgresql -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres`
`docker pull postgres`

docker run --name postgres-db \
  -e POSTGRES_PASSWORD=lia.1102 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=postgres \
  -p 5431:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres

  docker exec -e AIRFLOW__CORE__TEST_CONNECTION=Enabled 8cdf2446afa2 airflow connections test Test-dB


docker stop postgres-db
docker rm postgres-db

  docker run -d   --name postgres-db   --network airflow-docker_default   -p 5431:5432   -e POSTGRES_PASSWORD=lia.1102   postgres:15


En ocaciones se queda inhibido el contenedor de postgres, por lo que se debe eliminar y volver a crear.

`docker stop postgres-db`
`docker rm postgres-db`
`docker run -d   --name postgres-db   --network airflow-docker_default   -p 5431:5432   -e POSTGRES_PASSWORD=lia.1102   postgres:15`

o se puede detener y volver a iniciar:

docker stop postgres-db
docker start postgres-db