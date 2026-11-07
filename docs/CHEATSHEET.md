# TaskTrack Cheat Sheet

Your quick reference while learning. It gets updated as we go through each phase.

> **Tip:** to read this nicely formatted in VS Code, open this file and press `Ctrl + Shift + V`.

**Contents:** [Big picture](#1-the-big-picture) · [DevOps comparisons](#2-in-devops-terms) ·
[Daily commands](#3-daily-commands) · [Talking to the API](#4-talking-to-the-api) ·
[Status codes](#5-http-status-codes) · [Project files](#6-where-things-live) ·
[Glossary](#7-glossary) · [Troubleshooting](#8-troubleshooting) · [Lessons learned](#9-lessons-learned)

---

## 1. The big picture

```
  Website (localhost:3000)  ──┐
  Docs page (8000/docs)     ──┼── API request ──►  BACKEND  ────►  DATABASE
  curl in terminal          ──┘                   (the brain)      (the storage)
                                                   port 8000        port 5432
```

- **Frontend** = the screen you click on. It only *asks*. It never touches the database.
- **Backend** = the brain. It checks every request, applies the rules, and is the **only**
  thing that talks to the database.
- **Database** = permanent storage. Data survives restarts.
- **API** = the agreed list of requests the backend understands (`GET /tasks`, `POST /tasks`, …).

**Restaurant version:** frontend = dining room and waiter, backend = kitchen, database = pantry,
security = staff checking who's allowed in the kitchen.

---

## 2. In DevOps terms

| You already know | In this project | Role |
|---|---|---|
| Editor you write playbooks in | **VS Code** | Where you write and change things |
| Ansible playbook | **Your code** + `docker-compose.yml` | The instructions |
| Jenkins / Ansible engine | **Docker** | Runs the instructions |
| Jenkins console output | Terminal logs / Docker Desktop | See what happened |
| Inventory + playbook | `docker-compose.yml` | Lists the "hosts" (db, backend, frontend) and how to run them |
| Ansible role (for one machine) | `Dockerfile` | Install this, copy that, run as this user |
| `group_vars` / `host_vars` | `.env` | Settings and secrets, kept out of the code |
| Ordering plays | `depends_on: service_healthy` | Don't start backend until db is ready |
| "Build Now" in Jenkins | `docker compose up --build` | Build and run |
| Jenkinsfile | GitHub Actions workflow (Phase 5) | CI/CD pipeline in YAML |
| `post { always { … } }` | `try / finally` in Python | Always runs, even after an error |

---

## 3. Daily commands

### Start and stop the app
| What | Command | Notes |
|---|---|---|
| Start (first time, or after code changes) | `docker compose up --build` | Docker Desktop must say **Engine running** |
| Start (no code changes) | `docker compose up` | Faster |
| Start in background | `docker compose up -d` | Gives you your terminal back |
| Stop (while it's running in the terminal) | `Ctrl + C` | |
| Stop and clean up containers | `docker compose down` | ✅ Keeps your data |
| ⚠️ Stop and **delete all data** | `docker compose down -v` | `-v` deletes the database volume |

### Check on things
| What | Command |
|---|---|
| What's running? | `docker compose ps` |
| Backend logs | `docker compose logs backend --tail 30` |
| Follow logs live | `docker compose logs -f` |
| Look inside the database | `docker compose exec db psql -U tasktrack -c "SELECT * FROM tasks;"` |
| Open a database shell | `docker compose exec db psql -U tasktrack` (type `\q` to exit) |

### Git (saving your work to GitHub)
| What | Command |
|---|---|
| What changed? | `git status` |
| Get latest from GitHub | `git pull` |
| Stage all changes | `git add .` |
| Save a snapshot | `git commit -m "Describe what you changed"` |
| Upload to GitHub | `git push` |
| Undo changes to one file (careful) | `git restore path/to/file` |
| See history | `git log --oneline` |

### Addresses
| Address | What |
|---|---|
| http://localhost:3000 | The website |
| http://localhost:8000/docs | API test page |
| http://localhost:8000/health | "Are you alive?" check |

### Coming back after a break
1. Open **Docker Desktop**, wait for **Engine running**.
2. Open the project in VS Code (Git Bash terminal).
3. `git pull` to get the latest changes.
4. `docker compose up`, adding `--build` if `git pull` brought new code.
5. Open http://localhost:3000

---

## 4. Talking to the API

### The four actions (CRUD)
| Action | HTTP method | URL | Plain English |
|---|---|---|---|
| **C**reate | `POST` | `/tasks` | "Save this new task" |
| **R**ead | `GET` | `/tasks` or `/tasks/2` | "Give me all tasks" / "give me task 2" |
| **U**pdate | `PATCH` | `/tasks/2` | "Change part of task 2" |
| **D**elete | `DELETE` | `/tasks/2` | "Remove task 2" |

### Same actions with curl (Git Bash)
```bash
# List all tasks
curl http://localhost:8000/tasks

# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "My task", "description": "Optional details"}'

# Mark task 2 done (PATCH only changes the fields you send)
curl -X PATCH http://localhost:8000/tasks/2 -H "Content-Type: application/json" -d '{"done": true}'

# Delete task 2
curl -X DELETE http://localhost:8000/tasks/2
```

**curl parts:** `-X` = which action · `-H` = header ("I'm sending JSON") · `-d` = the data you send

### Using the docs page (localhost:8000/docs)
1. Click a row (e.g. **POST /tasks**) → **Try it out**
2. In the Request body box: **Ctrl + A**, then **Delete**, then paste your JSON. ⚠️ Don't leave the `"string"` example text!
3. **Execute** → read **Server response** (not "Example Value")

---

## 5. HTTP status codes

| Code | Meaning | You'll see it when… |
|---|---|---|
| **200** | OK | Read or update worked |
| **201** | Created | New task saved |
| **204** | No Content | Delete worked (nothing to send back) |
| **401** | Unauthorized | Not logged in *(Phase 3)* |
| **403** | Forbidden | Logged in, but not allowed *(Phase 3)* |
| **404** | Not Found | That task id doesn't exist |
| **422** | Unprocessable | Your data broke the rules (e.g. empty title) |
| **500** | Server Error | A bug in the backend: check `docker compose logs backend` |

**Rule of thumb:** 2xx = success · 4xx = the *request* was wrong · 5xx = the *server* broke

---

## 6. Where things live

```
tasktrack/
├── .env                  Your settings and passwords (NEVER on GitHub)
├── .env.example          Template for .env (safe to share)
├── docker-compose.yml    Runs all 3 containers together
├── backend/              The brain (Python + FastAPI)
│   ├── Dockerfile
│   ├── requirements.txt  Python packages (like a shopping list)
│   └── app/
│       ├── config.py         Reads settings from .env
│       ├── database.py       Connects to Postgres
│       ├── models.py         Database tables
│       ├── schemas.py        Rules for data in and out (the bouncer)
│       ├── routers/tasks.py  The actions: list, create, update, delete
│       └── main.py           Starts the app, CORS, /health
├── frontend/             The screen (React + TypeScript)
│   ├── Dockerfile
│   ├── package.json      JavaScript packages
│   └── src/
│       ├── api.ts            ★ The bridge: the only file that calls the backend
│       ├── types.ts          What a Task looks like
│       ├── App.tsx           Main screen
│       └── components/       TaskForm (add box), TaskItem (one row)
└── docs/                 Lessons + this cheat sheet
```

**"I want to change…"**
| …the data stored for a task | `models.py` + `schemas.py` (+ `types.ts` on the frontend) |
| …what the API does | `routers/tasks.py` |
| …how the page looks | `frontend/src/styles.css` |
| …what's on the screen | `App.tsx` or `components/` |
| …a setting or password | `.env` |

---

## 7. Glossary

| Word | Plain English |
|---|---|
| **API** | The list of requests a backend understands, and how to ask. |
| **Endpoint** | One item on that list, e.g. `POST /tasks`. |
| **JSON** | The text format data travels in: `{"title": "Buy milk", "done": false}` |
| **CRUD** | Create, Read, Update, Delete: what almost every app does. |
| **HTTP method** | The *type* of request: GET, POST, PATCH, DELETE. |
| **Status code** | The number the backend replies with (200, 404, …). |
| **Request body** | The data you send with a request (the `-d` part in curl). |
| **Framework** | A toolkit that handles the boring parts. FastAPI (backend), React (frontend). |
| **ORM** (SQLAlchemy) | Lets you use Python classes instead of writing SQL. Also blocks SQL injection. |
| **Model** | A Python class that describes a database table. |
| **Schema** | The rules for what data may come in and go out of the API. |
| **Validation** | Checking data before using it (empty title → 422). |
| **Commit (database)** | `db.commit()`: actually save the changes. Like `git commit`. |
| **Component** | A reusable piece of screen in React (e.g. one task row). |
| **State** | Data in React that redraws the screen when it changes. |
| **Props** | Inputs passed from a parent component to a child. |
| **Origin** | Protocol + address + port. `localhost:3000` and `localhost:8000` are different origins. |
| **CORS** | Backend's list of websites the browser may let call it. Protects users. |
| **XSS** | Attack: sneaking code into a page. React blocks it by showing text as text. |
| **SQL injection** | Attack: sneaking SQL into a form field. The ORM blocks it. |
| **Container** | A packaged, isolated app with everything it needs to run. |
| **Image** | The template a container is created from (built from a Dockerfile). |
| **Volume** | Docker storage that survives restarts (where the database keeps its data). |
| **Multi-stage build** | Dockerfile that builds in one image, then copies only the result into a small final image. |
| **Environment variable** | A setting passed to a program from outside its code (e.g. `DATABASE_URL`). |
| **localhost** | "This computer." |
| **Port** | A numbered door on a computer. Each service listens on its own (3000, 8000, 5432). |

---

## 8. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop not running | Open Docker Desktop, wait for **Engine running** |
| `docker: command not found` | Docker not installed, or old terminal | Install Docker Desktop. Open a **new** terminal. |
| `port is already allocated` | Something else uses 3000/8000/5432 | Stop the other program, or change the left-hand port in `docker-compose.yml` |
| Website shows "Failed to fetch" | Backend not running | `docker compose ps`, then `docker compose logs backend` |
| CORS error in browser console (F12) | Website's address not in `CORS_ORIGINS` | Check `.env`, then restart the backend |
| My code change isn't showing | Image not rebuilt | `docker compose up --build` |
| Task title became `"string"` | Example text left in docs page box | **Ctrl + A** → Delete before pasting |
| Same task appeared twice | Clicked Execute twice | Delete one: `curl -X DELETE http://localhost:8000/tasks/<id>` |
| All my tasks disappeared | Ran `docker compose down -v` | `-v` deletes data. Use plain `docker compose down`. |
| Git Bash not in VS Code | VS Code started before Git was installed | Restart VS Code, then `Ctrl+Shift+P` → *Terminal: Select Default Profile* → Git Bash |

**When stuck:** read the **last 20 lines** of the terminal. The real error is usually near the bottom.

---

## 9. Lessons learned

Things you discovered by doing:

1. **The backend does exactly what you send it**, even a duplicate or a title of `"string"`.
   That's why apps need validation and careful design.
2. **PATCH only changes the fields you send.** Everything else stays as it was.
3. **Database ids are never reused**, even after a delete.
4. **Frontend checks are for convenience, the backend is the real guard.** Anyone can skip the
   website and use curl.
5. **The docs page, the website and curl all send the same API requests.** They're just
   different ways of asking.
6. **Use Docker for things you don't edit** (like the database), and run the code you're
   changing directly for instant feedback. *(We'll set this up in Phase 3.)*

---

## Progress

| Phase | Topic | Status |
|---|---|---|
| 1 | Backend + database | ✅ Built · [lesson](01-backend.md) |
| 2 | Frontend | ✅ Built · [lesson](02-frontend.md) |
| — | Laptop setup (VS Code, Git Bash, Docker, Claude) | ✅ Done |
| — | Task 1: Explore the API (CRUD by hand) | ✅ Done |
| — | Task 2: Watch frontend talk to backend (F12) | ⏳ Next |
| — | Task 3: Look inside the database | ⏳ |
| 3 | User accounts and login | ⏳ |
| 4 | Security hardening | ⏳ |
| 5 | Tests + CI/CD pipeline | ⏳ |
| 6 | Deploy to the cloud (AWS) | ⏳ |
