# Lumio demo API

Tiny Flask service over a local SQLite product catalog. Built to demo two
GitHub capabilities in a first technical meeting:

- **Beat 1 (velocity):** Copilot completes `format_price` from its docstring.
- **Beat 2 (safety):** CodeQL + Copilot Autofix catch a SQL injection in a PR.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Then:

```bash
curl "http://127.0.0.1:5000/products"
curl "http://127.0.0.1:5000/product?id=1"
# The vuln (do NOT ship this): dumps all rows
curl "http://127.0.0.1:5000/product?id=0%20OR%201=1"
```

## The two demo surfaces

| Endpoint    | State      | Used for                                   |
|-------------|------------|--------------------------------------------|
| `/products` | clean      | calls `format_price` (Copilot completes it)|
| `/product`  | vulnerable | CWE-89 SQL injection -> CodeQL + Autofix    |

See `RUNBOOK.md` for the live choreography.
