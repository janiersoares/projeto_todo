# To-Do List API

HTTP API to register users, log in, and manage personal tasks on Postgres. Each user can only see their own tasks.

[![tests](https://github.com/janiersoares/projeto_todo/actions/workflows/tests.yml/badge.svg)](https://github.com/janiersoares/projeto_todo/actions/workflows/tests.yml)

## Requirements

- Python 3.10 or higher
- A Postgres database (this project was developed with Neon)

## How to run

### Option 1: with Docker

Requires Docker Desktop. Create a `.env` file with `JWT_SECRET` (see step 2 below), then run:

```bash
docker compose up --build
```

The API runs at `http://localhost:8000` and the database at `localhost:5432`.

### Option 2: locally

1. Install the dependencies:

   ```bash
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\activate

   # Any system
   pip install -r requirements.txt
   ```

2. Create a file named `.env` in the project root:

   ```
   DATABASE_URL=postgresql://user:password@host/neondb?sslmode=require
   JWT_SECRET=replace-with-a-long-secret-of-at-least-32-characters
   ```

   - `DATABASE_URL`: your database connection string, without quotes and without spaces around the `=`.
   - `JWT_SECRET`: the key used to sign the tokens. To generate a new one, run:

     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```

   Git ignores `.env`, so the password and the secret never reach GitHub.

3. Apply the migrations:

   ```bash
   python migrate.py
   ```

4. Start the server:

   ```bash
   uvicorn main:app --env-file .env
   ```

5. Open the interactive documentation at `http://127.0.0.1:8000/docs`.

## Authentication

The flow is: register, log in, get a token, and send it on the task routes.

### Register: `POST /auth/register`

Body (JSON):

```json
{
  "email": "ana@example.com",
  "password": "password123"
}
```

- `201`: user created. Returns `id`, `email`, and `created_at`.
- `409`: the email is already registered.
- `422`: invalid email or a password shorter than 8 characters.

Emails are stored in lowercase, so `Ana@Example.com` and `ana@example.com` are the same account.

### Log in: `POST /auth/login`

Body (JSON), same as register.

- `200`: returns the token, in the format `{"access_token": "...", "token_type": "bearer"}`.
- `401`: invalid email or password.
- `429`: too many failed attempts for this email. See below.

### Login rate limit

After 5 failed attempts for the same email within 15 minutes, login returns `429` until the window passes. A successful login clears the counter. The counter lives in the server's memory, so it resets when the server restarts.

Design trade-offs of this limit:

- **Anyone who knows an email can lock that account for 15 minutes** by failing on purpose. This is the usual price of protecting against password guessing. A stronger version would limit by IP address as well.
- **The counter is per process.** With several workers, each one counts on its own. A shared store such as Redis would fix this.

### Using the token

Send the token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

The token expires after 30 minutes. After that, the routes return `401` and you need to log in again.

## Tasks

All task routes require the `Authorization` header. Without it, the response is `401`.

| Method | Route | Action |
|---|---|---|
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List your tasks (paginated) |
| `GET` | `/tasks/{id}` | Get one task |
| `PUT` | `/tasks/{id}` | Update title and description |
| `PATCH` | `/tasks/{id}/status` | Change the status |
| `DELETE` | `/tasks/{id}` | Delete a task |

A task's status is `pending` or `completed`. Tasks that belong to another user return `404`, as if they did not exist. The fields for each request are described in `/docs`.

### Pagination

`GET /tasks` accepts two optional query parameters:

- `limit`: how many tasks to return, from 1 to 100. Default: 20.
- `offset`: how many tasks to skip. Default: 0.

Example: `GET /tasks?limit=10&offset=20` returns tasks 21 to 30 of your list. Tasks are ordered by `id`.

## Tests

With your `.env` configured, run:

```bash
python -m pytest -v
```

The tests use the real database. Each test rolls back its own changes when it finishes.

Tests also run automatically on GitHub Actions for every pull request, using a Postgres service container.

## Project structure

- `routes/`: HTTP endpoints
- `schemas/`: validation of input and output data
- `services/`: business rules
- `repositories/`: SQL queries
- `security/`: password hashing (bcrypt), tokens (JWT), login rate limit, and the dependency that identifies the user
- `migrations/`: database changes, applied in order on startup
- `tests/`: automated tests
- `.github/workflows/`: continuous integration

## License

MIT. See [LICENSE](LICENSE).
