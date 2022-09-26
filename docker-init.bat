wsl mkdir -p dags logs data plugins common
wsl sudo chown 50000:50000 dags logs data plugins common
wsl sudo chmod -R 777 dags logs data plugins common
wsl echo -e "AIRFLOW_UID=$(id -u)" > .env