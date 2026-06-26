"""
interfaces.py — Abstract base classes / interfaces for Mini Mart Management System
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


# ── Data Transfer Objects ──────────────────────────────────────────────────────

@dataclass
class ProductDTO:
    product_id:   Optional[int]
    name:         str
    category:     str
    price:        float
    cost:         float          # purchase / expense cost
    stock:        int
    created_at:   Optional[datetime] = None


@dataclass
class SaleItemDTO:
    product_id: int
    product_name: str
    quantity:   int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class SaleDTO:
    sale_id:    Optional[int]
    items:      List[SaleItemDTO]
    sale_date:  datetime
    total:      float


@dataclass
class ReportDTO:
    period_label: str          # e.g. "Week 24 – 2026" or "June 2026"
    income:       float        # total revenue from sales
    expense:      float        # total cost of goods sold
    profit:       float        # income - expense
    num_sales:    int


# ── Repository Interfaces ──────────────────────────────────────────────────────

class IProductRepository(ABC):
    @abstractmethod
    def add(self, product: ProductDTO) -> ProductDTO: ...

    @abstractmethod
    def update_stock(self, product_id: int, quantity_delta: int) -> None: ...

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[ProductDTO]: ...

    @abstractmethod
    def search(self, term: str) -> List[ProductDTO]: ...

    @abstractmethod
    def get_all(self) -> List[ProductDTO]: ...


class ISaleRepository(ABC):
    @abstractmethod
    def record(self, sale: SaleDTO) -> SaleDTO: ...

    @abstractmethod
    def get_weekly_report(self, year: int, week: int) -> ReportDTO: ...

    @abstractmethod
    def get_monthly_report(self, year: int, month: int) -> ReportDTO: ...


# ── Service Interfaces ─────────────────────────────────────────────────────────

class IInventoryService(ABC):
    @abstractmethod
    def add_product(self, product: ProductDTO) -> ProductDTO: ...

    @abstractmethod
    def restock(self, product_id: int, quantity: int) -> None: ...

    @abstractmethod
    def search_products(self, term: str) -> List[ProductDTO]: ...

    @abstractmethod
    def list_all(self) -> List[ProductDTO]: ...


class ISalesService(ABC):
    @abstractmethod
    def process_sale(self, items: List[SaleItemDTO]) -> SaleDTO: ...

    @abstractmethod
    def weekly_report(self, year: int, week: int) -> ReportDTO: ...

    @abstractmethod
    def monthly_report(self, year: int, month: int) -> ReportDTO: ...
