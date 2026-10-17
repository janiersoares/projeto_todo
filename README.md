# To-Do List API

API HTTP para criar, listar, buscar, atualizar, mudar o status e apagar tarefas no Postgres.

## Como executar

1. Instale as dependências:

   ```bash
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\activate

   # Em qualquer sistema
   pip install -r requirements.txt
   ```

2. Crie um arquivo chamado `.env` na pasta principal do projeto,
   com uma única linha:

   ```
   DATABASE_URL=postgresql://usuario:senha@endereco-do-banco/neondb?sslmode=require
   ```

   Troque o valor pela connection string do seu banco, sem aspas e sem espaços ao redor do `=`. O Git ignora esse arquivo, então a senha não vai pro GitHub.

3. Aplique as migrations:

   ```bash
   python migrate.py
   ```

4. Suba o servidor:

   ```bash
   uvicorn main:app --env-file .env
   ```

## Rotas

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{id}`
- `PUT /tasks/{id}`
- `PATCH /tasks/{id}/status`
- `DELETE /tasks/{id}`

O status de uma tarefa é `pending` ou `completed`.
