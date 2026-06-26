"""
db.py — SQLite persistence layer implementing IProductRepository & ISaleRepository
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

from core.interfaces import (
    IProductRepository, ISaleRepository,
    ProductDTO, SaleDTO, SaleItemDTO, ReportDTO,
)

DB_PATH = "mini_mart.db"


@contextmanager
def _connect(path: str = DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(path: str = DB_PATH) -> None:
    """Create tables if they do not exist."""
    with _connect(path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                product_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                price       REAL    NOT NULL CHECK(price >= 0),
                cost        REAL    NOT NULL CHECK(cost >= 0),
                stock       INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sales (
                sale_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date   TEXT    NOT NULL,
                total       REAL    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id     INTEGER NOT NULL REFERENCES sales(sale_id),
                product_id  INTEGER NOT NULL REFERENCES products(product_id),
                product_name TEXT   NOT NULL,
                quantity    INTEGER NOT NULL,
                unit_price  REAL    NOT NULL
            );
        """)


# ── Product Repository ─────────────────────────────────────────────────────────

class ProductRepository(IProductRepository):
    def __init__(self, path: str = DB_PATH):
        self._path = path

    def add(self, product: ProductDTO) -> ProductDTO:
        now = datetime.now().isoformat()
        with _connect(self._path) as conn:
            cur = conn.execute(
                "INSERT INTO products (name, category, price, cost, stock, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (product.name, product.category, product.price,
                 product.cost, product.stock, now),
            )
            product.product_id = cur.lastrowid
            product.created_at = datetime.fromisoformat(now)
        return product

    def update_stock(self, product_id: int, quantity_delta: int) -> None:
        with _connect(self._path) as conn:
            conn.execute(
                "UPDATE products SET stock = stock + ? WHERE product_id = ?",
                (quantity_delta, product_id),
            )

    def get_by_id(self, product_id: int) -> Optional[ProductDTO]:
        with _connect(self._path) as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE product_id = ?", (product_id,)
            ).fetchone()
        return self._row_to_dto(row) if row else None

    def search(self, term: str) -> List[ProductDTO]:
        like = f"%{term}%"
        with _connect(self._path) as conn:
            # search by name, category, or exact product_id
            rows = conn.execute(
                "SELECT * FROM products WHERE name LIKE ? OR category LIKE ? "
                "OR CAST(product_id AS TEXT) = ? ORDER BY name",
                (like, like, term),
            ).fetchall()
        return [self._row_to_dto(r) for r in rows]

    def get_all(self) -> List[ProductDTO]:
        with _connect(self._path) as conn:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY name"
            ).fetchall()
        return [self._row_to_dto(r) for r in rows]

    @staticmethod
    def _row_to_dto(row: sqlite3.Row) -> ProductDTO:
        return ProductDTO(
            product_id=row["product_id"],
            name=row["name"],
            category=row["category"],
            price=row["price"],
            cost=row["cost"],
            stock=row["stock"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )


# ── Sale Repository ────────────────────────────────────────────────────────────

class SaleRepository(ISaleRepository):
    def __init__(self, path: str = DB_PATH):
        self._path = path

    def record(self, sale: SaleDTO) -> SaleDTO:
        now = sale.sale_date.isoformat()
        with _connect(self._path) as conn:
            cur = conn.execute(
                "INSERT INTO sales (sale_date, total) VALUES (?, ?)",
                (now, sale.total),
            )
            sale.sale_id = cur.lastrowid
            for item in sale.items:
                conn.execute(
                    "INSERT INTO sale_items "
                    "(sale_id, product_id, product_name, quantity, unit_price) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (sale.sale_id, item.product_id, item.product_name,
                     item.quantity, item.unit_price),
                )
                # deduct stock
                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE product_id = ?",
                    (item.quantity, item.product_id),
                )
        return sale

    def get_weekly_report(self, year: int, week: int) -> ReportDTO:
        with _connect(self._path) as conn:
            row = conn.execute("""
                SELECT
                    COALESCE(SUM(s.total), 0)                          AS income,
                    COALESCE(SUM(si.quantity * p.cost), 0)             AS expense,
                    COUNT(DISTINCT s.sale_id)                          AS num_sales
                FROM sales s
                JOIN sale_items si ON si.sale_id = s.sale_id
                JOIN products   p  ON p.product_id = si.product_id
                WHERE CAST(strftime('%Y', s.sale_date) AS INTEGER) = ?
                  AND CAST(strftime('%W', s.sale_date) AS INTEGER) = ?
            """, (year, week)).fetchone()
        return self._build_report(f"Week {week:02d} – {year}", row)

    def get_monthly_report(self, year: int, month: int) -> ReportDTO:
        with _connect(self._path) as conn:
            row = conn.execute("""
                SELECT
                    COALESCE(SUM(s.total), 0)                          AS income,
                    COALESCE(SUM(si.quantity * p.cost), 0)             AS expense,
                    COUNT(DISTINCT s.sale_id)                          AS num_sales
                FROM sales s
                JOIN sale_items si ON si.sale_id = s.sale_id
                JOIN products   p  ON p.product_id = si.product_id
                WHERE CAST(strftime('%Y', s.sale_date) AS INTEGER) = ?
                  AND CAST(strftime('%m', s.sale_date) AS INTEGER) = ?
            """, (year, month)).fetchone()
        month_name = datetime(year, month, 1).strftime("%B %Y")
        return self._build_report(month_name, row)

    @staticmethod
    def _build_report(label: str, row: sqlite3.Row) -> ReportDTO:
        income  = float(row["income"])
        expense = float(row["expense"])
        return ReportDTO(
            period_label=label,
            income=income,
            expense=expense,
            profit=income - expense,
            num_sales=int(row["num_sales"]),
        )
