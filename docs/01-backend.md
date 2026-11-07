# Phase 1: Backend API + Database

## What a backend actually is

A backend is a program that listens on a port and answers HTTP requests, the same way
Jenkins answers on port 8080. When a request comes in, it:

1. **Checks the input** (is this valid JSON? is the title too long?)
2. **Applies rules** (later: is this user allowed to do this?)
3. **Talks to the database** (save or fetch data)
4. **Sends back a response**: JSON plus a status code

## Follow one request through the code

`POST /tasks` with body `{"title": "Buy milk"}`:

```
uvicorn (web server, port 8000)
  -> main.py              routes /tasks/* to routers/tasks.py
  -> schemas.TaskCreate   validates the JSON (title 1-200 chars). Bad input stops here with a 422.
  -> database.get_db      opens a DB session
  -> tasks.create_task    builds a Task object, db.add(), db.commit()
  -> models.Task          SQLAlchemy turns this into: INSERT INTO tasks (title) VALUES ($1)
  -> PostgreSQL           stores the row, generates id and created_at
  -> schemas.TaskOut      shapes the response JSON
  <- 201 Created  {"id": 1, "title": "Buy milk", "done": false, ...}
```

Read the files in this order: `config.py` → `database.py` → `models.py` → `schemas.py`
→ `routers/tasks.py` → `main.py`. Each one is short and commented.

## HTTP status codes you'll see

| Code | Meaning | When |
|---|---|---|
| 200 | OK | Successful GET/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 404 | Not Found | Task id doesn't exist |
| 422 | Unprocessable | Your JSON failed validation |
| 500 | Server Error | A bug in our code |

## Why a database (and why Postgres)?

Without one, data lives in the program's memory and disappears on every restart or
deploy. A relational database gives you:

- **Persistence**: data lives on disk, in a Docker volume here.
- **Transactions**: `db.commit()` is all-or-nothing, so you never get half a write.
- **Concurrency**: many requests can read and write safely at the same time.
- **Relations**: in Phase 3, every task will belong to a user, and Postgres enforces that link.

## Security already in place

- **Input validation**: Pydantic schemas reject malformed or oversized input.
- **SQL injection protection**: the ORM sends values as parameters, never pasted into SQL text.
- **Secrets outside code**: credentials live in `.env`, which git ignores.
- **Container doesn't run as root**: see `USER appuser` in the Dockerfile.
- **Not yet**: anyone can read or delete any task. Phase 3 fixes that with logins.

## Run it

```bash
cp .env.example .env
docker compose up --build
```

- Open **http://localhost:8000/docs**. This is interactive API documentation, and you can
  click "Try it out" on each endpoint.
- Or use curl:

```bash
curl -X POST localhost:8000/tasks -H 'Content-Type: application/json' -d '{"title":"Learn FastAPI"}'
curl localhost:8000/tasks
```

- Look inside the database directly:

```bash
docker compose exec db psql -U tasktrack -c 'SELECT * FROM tasks;'
```

## Exercises: do these yourself, that's where the learning is

1. **Add a field.** Add `priority` (an int from 1 to 3, default 2) to the model and all three
   schemas. Restart. Notice that the existing table *doesn't* get the new column, because
   `create_all` only creates missing tables. Run `docker compose down -v` to wipe the data and try
   again. That pain is exactly why Phase 3 introduces migrations.
2. **Add a filter.** Make `GET /tasks?done=true` return only completed tasks. Hint: add
   `done: bool | None = None` as a function parameter, then use `.where(Task.done == done)`.
3. **Break it on purpose.** Stop the db container while the backend runs, call the API, and
   read the error in `docker compose logs backend`. Then start db again. Did it recover?
   (`pool_pre_ping` in `database.py` is why it does.)
4. **Read the SQL.** Add `echo=True` to `create_engine(...)` and watch the logs show every
   SQL statement the ORM generates.
