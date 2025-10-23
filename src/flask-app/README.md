# Flask App Example

This demo shows a simple form → submit → landing page flow.

Routes:
- `GET /` — Shows a profile form (name, email, role, bio, subscribe)
- `POST /submit` — Validates and redirects via PRG pattern
- `GET /welcome` — Displays submitted information

Run (dev):

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py  # or: flask run
```

Open http://127.0.0.1:5000/