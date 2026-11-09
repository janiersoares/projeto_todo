# To-Do List API

HTTP API to register users, log in, and manage personal tasks on Postgres (Neon). Each user can only see their own tasks.

## Requirements

- Python 3.10 or higher
- A Postgres database (this project uses Neon)

## How to run

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

### Log in: `POST /auth/login`

Body (JSON), same as register.

- `200`: returns the token, in the format `{"access_token": "...", "token_type": "bearer"}`.
- `401`: invalid email or password.

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
| `GET` | `/tasks` | List your tasks |
| `GET` | `/tasks/{id}` | Get one task |
| `PUT` | `/tasks/{id}` | Update title and description |
| `PATCH` | `/tasks/{id}/status` | Change the status |
| `DELETE` | `/tasks/{id}` | Delete a task |

A task's status is `pending` or `completed`. Tasks that belong to another user return `404`, as if they did not exist. The fields for each request are described in `/docs`.

## Tests

With your `.env` configured, run:

```bash
python -m pytest -v
```

The tests use the real database. Each test rolls back its own changes when it finishes.

## Project structure

- `routes/`: HTTP endpoints
- `schemas/`: validation of input and output data
- `services/`: business rules
- `repositories/`: SQL queries
- `security/`: password hashing (bcrypt), tokens (JWT), and the dependency that identifies the user
- `migrations/`: database changes, applied in order
- `tests/`: automated tests