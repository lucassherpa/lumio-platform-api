"""Lumio product catalog API.

Tiny Flask service over a local SQLite product catalog.
"""

import sqlite3

from flask import Flask, jsonify

app = Flask(__name__)

DB_PATH = "catalog.db"


def get_connection() -> sqlite3.Connection:
    """Open a connection to the SQLite catalog with row access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
