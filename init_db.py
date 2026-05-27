"""Create and seed the local SQLite catalog for the demo."""

import sqlite3

DB_PATH = "catalog.db"

PRODUCTS = [
    (1, "Espresso Beans 1kg", 1999),
    (2, "Cold Brew Bottle", 500),
    (3, "Ceramic Mug", 1250),
]


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS products")
    conn.execute(
        "CREATE TABLE products ("
        "id INTEGER PRIMARY KEY, "
        "name TEXT NOT NULL, "
        "price_cents INTEGER NOT NULL)"
    )
    conn.executemany(
        "INSERT INTO products (id, name, price_cents) VALUES (?, ?, ?)",
        PRODUCTS,
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(PRODUCTS)} products into {DB_PATH}")


if __name__ == "__main__":
    main()
