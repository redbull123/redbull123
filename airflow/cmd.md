**To run Airflow**
`docker compose up -d`

**To stop Airflow**
`docker compose down`

**To access Airflow UI**
`http://localhost:8080`

**To access Airflow CLI**
`docker compose exec api-server airflow`
docker compose exec pip install apache-airflow-providers-postgres

**To refresh all dags**
`docker exec -it airflow-docker-airflow-scheduler-1 airflow dags report`

**To check the dags files**
`docker compose exec api-server ls -l /opt/airflow/dags`
`docker exec -it  airflow-docker-airflow-scheduler-1 ls /opt/airflow/dags`

# Common commands
docker exec -it airflow-docker-airflow-scheduler-1 pip install apache-airflow-providers-postgres

or
docker exec -it airflow-docker-airflow-scheduler-1 bash

pip install apache-airflow-providers-postgres
