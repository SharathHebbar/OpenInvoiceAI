# Why Celery instead of FastAPI BackgroundTasks?

- BackgroundTasks don't scale across workers.
- Celery supports retries, scheduling, and distributed execution.
- Trade-off: Added operational complexity.