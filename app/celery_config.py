from celery import Celery
import logging


logger = logging.getLogger("celery")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"],
)

app.conf.beat_schedule = {
    "fetch-users": {
        "task": "app.tasks.fetch_users",
        "schedule": 15.0,
    },
    "fetch-address-credit-card": {
        "task": "app.tasks.fetch_address_credit_card",
        "schedule": 25.0,
    },
}

app.conf.timezone = "UTC"
