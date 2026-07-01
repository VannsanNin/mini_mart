"""
main.py — Entry point for Mini Mart Management System
"""
import sys
import os

# Make sure local packages resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

from database.db import init_db, ProductRepository
from core.services import InventoryService
from gui.app import MiniMartApp

if __name__ == "__main__":
    init_db()

    p_repo = ProductRepository()
    inv    = InventoryService(p_repo)

    app = MiniMartApp()
    app.mainloop()
