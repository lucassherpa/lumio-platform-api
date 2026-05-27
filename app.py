"""Lumio demo API.

Tiny Flask service over a local SQLite product catalog.
Two demo surfaces live here:

  1. /products            -> CLEAN. Copilot "velocity" beat.
                             A docstring-only stub for live completion.
  2. /product             -> VULNERABLE. CodeQL + Autofix beat.
                             Classic SQL injection (CWE-89).
"""

import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

DB_PATH = "catalog.db"


def get_connection() -> sqlite3.Connection:
    """Open a connection to the SQLite catalog with row access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# COPILOT DEMO SPOT  (Beat 1 - velocity)
# Live-complete the body from the docstring with Copilot in VS Code.
# Leave the body empty during the demo, then accept the suggestion.
# ---------------------------------------------------------------------------
def format_price(amount_cents: int, currency: str = "EUR") -> str:
    """Format an integer amount of cents into a human-readable price string.

    Converts cents to a major-unit amount with two decimals and appends the
    currency code. For example, 1999 with currency "EUR" returns "19.99 EUR",
    and 500 with currency "USD" returns "5.00 USD".

    Args:
        amount_cents: The price in integer cents (e.g. 1999).
        currency: The ISO 4217 currency code to append (default "EUR").

    Returns:
        A formatted price string like "19.99 EUR".
    """
    # <-- Copilot completes here during the live demo


@app.route("/products")
def list_products():
    """Return the full product catalog as JSON."""
    conn = get_connection()
    rows = conn.execute("SELECT id, name, price_cents FROM products").fetchall()
    conn.close()
    products = [
        {
            "id": row["id"],
            "name": row["name"],
            "price": format_price(row["price_cents"]),
        }
        for row in rows
    ]
    return jsonify(products)


# ---------------------------------------------------------------------------
# VULNERABLE ENDPOINT  (Beat 2 - catch + Autofix)
# CWE-89 SQL injection: untrusted request input is concatenated straight
# into the SQL string. This is the kind of code an AI assistant will happily
# emit when asked for "a lookup by id". CodeQL flags it as py/sql-injection
# and Copilot Autofix rewrites it as a parameterized query.
# ---------------------------------------------------------------------------
@app.route("/product")
def get_product():
    """Look up a single product by its id (?id=...)."""
    product_id = request.args.get("id")
    conn = get_connection()
    query = f"SELECT id, name, price_cents FROM products WHERE id = {product_id}"
    row = conn.execute(query).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(
        {
            "id": row["id"],
            "name": row["name"],
            "price": format_price(row["price_cents"]),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
