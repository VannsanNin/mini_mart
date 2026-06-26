# 🛒 Mini Mart Management System

A desktop Python application for managing a small retail store, built with
**Tkinter** (GUI), **SQLite** (database), and clean OOP architecture.

---

## Project Structure

```
mini_mart/
├── main.py                  # Entry point + demo seed data
├── requirements.txt
│
├── core/                    # Domain layer
│   ├── interfaces.py        # Abstract classes (IProductRepository, ISalesService …)
│   └── services.py          # Business logic (InventoryService, SalesService)
│
├── database/                # Persistence layer
│   └── db.py                # SQLite repositories + schema init
│
└── gui/                     # Presentation layer
    └── app.py               # All Tkinter tabs and widgets
```

---

## Features

| Tab | What it does |
|-----|-------------|
| **Dashboard** | Overview cards (total products, low-stock count, monthly income) + full product table |
| **Inventory** | Add new products; restock existing ones |
| **Sales POS** | Cart-based point-of-sale — add items, confirm sale, stock auto-deducted |
| **Search** | Find products by Name, Product ID, or Category |
| **Reports** | Weekly and monthly Income / COGS / Profit / # Sales summaries |

---

## Architecture

```
GUI (Tkinter)
    │
    ▼
Services (IInventoryService / ISalesService)   ← interfaces.py
    │
    ▼
Repositories (IProductRepository / ISaleRepository)
    │
    ▼
SQLite (mini_mart.db)
```

Classes and interfaces used:
- **`IProductRepository`** / **`ISaleRepository`** — abstract base classes
- **`ProductRepository`** / **`SaleRepository`** — concrete SQLite implementations
- **`InventoryService`** / **`SalesService`** — business-logic layer
- **`ProductDTO`** / **`SaleDTO`** / **`SaleItemDTO`** / **`ReportDTO`** — data transfer objects

---

## Running

```bash
# Make sure Python 3.10+ and tkinter are installed
python main.py
```

On Ubuntu/Debian if tkinter is missing:
```bash
sudo apt install python3-tk
```

The SQLite database `mini_mart.db` is created automatically on first run, and
10 demo products with 3 sample sales are seeded so the app opens with data.
