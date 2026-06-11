from datetime import timedelta, datetime

from alert import task_failure_callback

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
    "on_failure_callback": task_failure_callback,
    "start_date": datetime(2026, 1, 1),
}
