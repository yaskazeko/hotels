from celery import Celery

from src.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    include=["src.tasks.tasks"],
)
