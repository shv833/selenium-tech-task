from celery import Celery

app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"],
)

app.conf.beat_schedule = {
    "fetch-users-every-hour": {
        "task": "app.tasks.fetch_users",
        "schedule": 10.0,
    },
    "fetch-address-credit-card-every-2-hours": {
        "task": "app.tasks.fetch_address_credit_card",
        "schedule": 11.0,
    },
}
app.conf.timezone = "UTC"
