"""
services.py — Business-logic services implementing IInventoryService & ISalesService
"""
from datetime import datetime
from typing import List

from core.interfaces import (
    IInventoryService, ISalesService,
    IProductRepository, ISaleRepository,
    ProductDTO, SaleDTO, SaleItemDTO, ReportDTO,
)


class InventoryService(IInventoryService):
    def __init__(self, repo: IProductRepository):
        self._repo = repo
        print(repo)

    def add_product(self, product: ProductDTO) -> ProductDTO:
        if not product.name.strip():
            raise ValueError("Product name cannot be empty.")
        if product.price < 0:
            raise ValueError("Price must be non-negative.")
        if product.cost < 0:
            raise ValueError("Cost must be non-negative.")
        if product.stock < 0:
            raise ValueError("Initial stock must be non-negative.")
        return self._repo.add(product)

    def restock(self, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive.")
        p = self._repo.get_by_id(product_id)
        if p is None:
            raise LookupError(f"Product ID {product_id} not found.")
        self._repo.update_stock(product_id, quantity)

    def search_products(self, term: str) -> List[ProductDTO]:
        return self._repo.search(term.strip())

    def list_all(self) -> List[ProductDTO]:
        return self._repo.get_all()


class SalesService(ISalesService):
    def __init__(self, sale_repo: ISaleRepository, product_repo: IProductRepository):
        self._sales    = sale_repo
        self._products = product_repo

    def process_sale(self, items: List[SaleItemDTO]) -> SaleDTO:
        if not items:
            raise ValueError("A sale must contain at least one item.")

        # Validate stock availability
        for item in items:
            p = self._products.get_by_id(item.product_id)
            if p is None:
                raise LookupError(f"Product ID {item.product_id} not found.")
            if p.stock < item.quantity:
                raise ValueError(
                    f"Insufficient stock for '{p.name}': "
                    f"available {p.stock}, requested {item.quantity}."
                )
            item.unit_price = p.price          # always use current price
            item.product_name = p.name

        total = sum(i.subtotal for i in items)
        sale  = SaleDTO(
            sale_id=None,
            items=items,
            sale_date=datetime.now(),
            total=total,
        )
        return self._sales.record(sale)

    def weekly_report(self, year: int, week: int) -> ReportDTO:
        return self._sales.get_weekly_report(year, week)

    def monthly_report(self, year: int, month: int) -> ReportDTO:
        return self._sales.get_monthly_report(year, month)
