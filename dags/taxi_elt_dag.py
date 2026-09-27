from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "kaoutar",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="taxi_elt_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["elt", "dbt", "snowflake", "portfolio"],
) as dag:

    # On utilise BashOperator pour exécuter le script Python directement
    ingest_task = BashOperator(
        task_id="ingest_raw_data",
        bash_command="python /opt/airflow/include/ingestion/download_raw.py",
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command="pip install dbt-snowflake && cd /opt/airflow/dbt_project && /home/airflow/.local/bin/dbt run --profiles-dir /opt/airflow/dbt_project",
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt_project && /home/airflow/.local/bin/dbt test --profiles-dir /opt/airflow/dbt_project",
    )

    # Ordre d'exécution
    ingest_task >> dbt_run_task >> dbt_test_task