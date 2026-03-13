## FastAPI Backend

A scalable backend structure using FastAPI

To run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4321 --reload
```

To migrate:

```bash
alembic revision --autogenerate -m "message here"
```

If above doesn't work then:

```bash
alembic upgrade head  # brings the database up to the latest revision

alembic revision --autogenerate -m "message here"
```
