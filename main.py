"""
main.py — Entry point for Mini Mart Management System
"""
import sys
import os

# Make sure local packages resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

from database.db import init_db, ProductRepository, SaleRepository
from core.services import InventoryService, SalesService
from core.interfaces import ProductDTO, SaleItemDTO
from gui.app import MiniMartApp


def _seed(inv: InventoryService, sales: SalesService) -> None:
    """Insert demo data only when the DB is empty."""
    if inv.list_all():
        return

    products = [
        ProductDTO(None, "Coca-Cola 330ml",     "Beverages",        1.25, 0.70, 120),
        ProductDTO(None, "Mineral Water 500ml", "Beverages",        0.60, 0.25, 200),
        ProductDTO(None, "Full-Cream Milk 1L",  "Dairy",            1.80, 1.10,  60),
        ProductDTO(None, "Cheddar Cheese 200g", "Dairy",            2.50, 1.60,  40),
        ProductDTO(None, "Lays Classic 75g",    "Snacks",           1.10, 0.55,  90),
        ProductDTO(None, "Jasmine Rice 5kg",    "Grains & Cereals", 6.50, 4.20,  30),
        ProductDTO(None, "Instant Noodles",     "Grains & Cereals", 0.45, 0.20, 150),
        ProductDTO(None, "Shampoo 200ml",       "Personal Care",    3.20, 1.80,  25),
        ProductDTO(None, "Dish Soap 500ml",     "Household",        1.50, 0.80,  45),
        ProductDTO(None, "Frozen Chicken 1kg",  "Frozen",           5.00, 3.40,  20),
    ]

    added = [inv.add_product(p) for p in products]

    # Record a few sample sales
    try:
        sales.process_sale([
            SaleItemDTO(added[0].product_id, "", 3, 0),
            SaleItemDTO(added[4].product_id, "", 2, 0),
        ])
        sales.process_sale([
            SaleItemDTO(added[2].product_id, "", 1, 0),
            SaleItemDTO(added[5].product_id, "", 2, 0),
        ])
        sales.process_sale([
            SaleItemDTO(added[6].product_id, "", 5, 0),
            SaleItemDTO(added[1].product_id, "", 4, 0),
        ])
    except Exception:
        pass   # Seed sales are optional


if __name__ == "__main__":
    init_db()

    p_repo = ProductRepository()
    s_repo = SaleRepository()
    inv    = InventoryService(p_repo)
    sal    = SalesService(s_repo, p_repo)

    _seed(inv, sal)

    app = MiniMartApp()
    app.mainloop()
