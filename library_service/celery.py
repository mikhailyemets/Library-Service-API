import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")

app = Celery("library_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "books_task": {
        "task": "books.tasks.scheduled_task",
        "schedule": crontab(hour=11, minute=52)  # TODO CHANGE FOR PROD
    },
    "borrowing_task": {
        "task": "borrowings.tasks.scheduled_task",
        "schedule": crontab(hour=11, minute=52),  # TODO CHANGE FOR PROD
    },
    "expired_borrowing": {
        "task": "borrowings.tasks.send_overdue_borrowings_notification",
        "schedule": crontab(hour=11, minute=52),  # TODO CHANGE FOR PROD
    }
}
