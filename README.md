# TaskTrack — a learning project

> 📌 **Quick reference:** [docs/CHEATSHEET.md](docs/CHEATSHEET.md) lists commands, terms, status codes and troubleshooting in one place.

A task tracker with user accounts, built from scratch one layer at a time.
The point isn't the app itself. A task tracker is small enough to finish, and it
still touches every layer a real product has: an API, a database, a UI, logins,
security, containers, and CI/CD.

## The stack, and why

| Layer | Choice | Why this one |
|---|---|---|
| Backend language | **Python** | You already read Python through Ansible (modules, Jinja2, filters). It's the most readable language to learn web concepts in, and it's heavily used in DevOps tooling. |
| Backend framework | **FastAPI** | Modern and fast, with built-in data validation. It generates interactive API docs at `/docs`, so you can test the API without writing a frontend first. |
| Database | **PostgreSQL** | The default choice for relational data. It's free, battle-tested, and available as a managed service on every cloud (RDS, Cloud SQL, Azure DB). |
| DB access | **SQLAlchemy** (ORM) | You write Python classes instead of raw SQL strings, and queries are parameterized automatically, which blocks SQL injection. |
| Frontend | **React + TypeScript (Vite)** | The most in-demand UI library. TypeScript catches mistakes before they reach the browser. |
| Packaging | **Docker + Docker Compose** | Your home turf. One command starts the whole stack. |
| CI/CD | **GitHub Actions** | Same ideas as Jenkins pipelines, configured in YAML. |

## How the pieces connect

```
 Browser (React)  --HTTP/JSON-->  FastAPI backend  --SQL-->  PostgreSQL
   port 5173                        port 8000                port 5432
```

- The **frontend** only draws screens. It never talks to the database directly.
- The **backend** holds the rules, such as "you can only see your own tasks". It's
  the only thing that touches the database.
- The **database** stores data so it survives restarts.

## Roadmap

| Phase | What you build | What you learn | Status |
|---|---|---|---|
| 1 | Backend API + database | REST, HTTP methods, ORM, validation, Docker Compose | ✅ [docs/01-backend.md](docs/01-backend.md) |
| 2 | Frontend | React components, state, calling an API, CORS | ✅ [docs/02-frontend.md](docs/02-frontend.md) |
| 3 | Users & login | Password hashing, JWT tokens, authorization, DB migrations | ⏳ |
| 4 | Security hardening | Secrets, HTTPS, rate limiting, OWASP Top 10, dependency scanning | ⏳ |
| 5 | Tests + CI/CD | pytest, GitHub Actions pipeline, building images | ⏳ |
| 6 | Deploy | Running it on a real server or cloud | ⏳ |

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

- App: http://localhost:3000
- API docs: http://localhost:8000/docs
