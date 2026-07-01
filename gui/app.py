"""
app.py — Main Tkinter GUI for Mini Mart Management System
"""
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from datetime import datetime

from core.interfaces import ProductDTO, SaleItemDTO
from core.services import InventoryService, SalesService
from database.db import ProductRepository, SaleRepository, init_db

# ── Theme system ───────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "BG":       "#0F1117",
        "SURFACE":  "#1A1D27",
        "SURFACE2": "#252836",
        "ACCENT":   "#4F8EF7",
        "SUCCESS":  "#3DDC97",
        "DANGER":   "#F75F4F",
        "WARNING":  "#F7C94F",
        "TEXT":     "#E8EAF0",
        "MUTED":    "#8890A4",
        "BORDER":   "#2E3247",
        "FOCUS":    "#2D3149",
        "BTN_ACTIVE":   "#3A6FD8",
        "BTN_PRESSED":  "#2C5AB8",
        "SUCC_ACTIVE":  "#2EB87A",
        "DANG_ACTIVE":  "#D44535",
    },
    "light": {
        "BG":       "#F5F6FA",
        "SURFACE":  "#FFFFFF",
        "SURFACE2": "#E2E5ED",
        "ACCENT":   "#3366CC",
        "SUCCESS":  "#28A745",
        "DANGER":   "#DC3545",
        "WARNING":  "#CC9200",
        "TEXT":     "#1C1E26",
        "MUTED":    "#6C7284",
        "BORDER":   "#D1D5E0",
        "FOCUS":    "#C8D0E0",
        "BTN_ACTIVE":   "#2952A3",
        "BTN_PRESSED":  "#1E3D7A",
        "SUCC_ACTIVE":  "#1E8432",
        "DANG_ACTIVE":  "#A82835",
    },
}

_current_theme = "dark"

def _set_theme(name):
    global _current_theme, BG, SURFACE, SURFACE2, ACCENT, SUCCESS, DANGER, WARNING, TEXT, MUTED, BORDER, FOCUS
    global BTN_ACTIVE, BTN_PRESSED, SUCC_ACTIVE, DANG_ACTIVE
    c = THEMES[name]
    BG       = c["BG"]
    SURFACE  = c["SURFACE"]
    SURFACE2 = c["SURFACE2"]
    ACCENT   = c["ACCENT"]
    SUCCESS  = c["SUCCESS"]
    DANGER   = c["DANGER"]
    WARNING  = c["WARNING"]
    TEXT     = c["TEXT"]
    MUTED    = c["MUTED"]
    BORDER   = c["BORDER"]
    FOCUS    = c["FOCUS"]
    BTN_ACTIVE  = c["BTN_ACTIVE"]
    BTN_PRESSED = c["BTN_PRESSED"]
    SUCC_ACTIVE = c["SUCC_ACTIVE"]
    DANG_ACTIVE = c["DANG_ACTIVE"]
    _current_theme = name

_set_theme("dark")


def _style(root: tk.Tk) -> None:
    """Configure ttk styles for the dark theme."""
    s = ttk.Style(root)
    s.theme_use("clam")

    common = {"background": SURFACE, "foreground": TEXT, "fieldbackground": SURFACE2,
               "bordercolor": BORDER, "lightcolor": BORDER, "darkcolor": BORDER,
               "troughcolor": SURFACE2, "relief": "flat"}

    s.configure("TFrame",       background=BG)
    s.configure("Card.TFrame",  background=SURFACE)
    s.configure("TLabel",       background=BG,      foreground=TEXT, font=("Segoe UI", 10))
    s.configure("Card.TLabel",  background=SURFACE, foreground=TEXT, font=("Segoe UI", 10))
    s.configure("Muted.TLabel", background=SURFACE, foreground=MUTED, font=("Segoe UI", 9))
    s.configure("Head.TLabel",  background=SURFACE, foreground=TEXT,
                font=("Segoe UI", 13, "bold"))
    s.configure("Stat.TLabel",  background=SURFACE, foreground=ACCENT,
                font=("Segoe UI", 22, "bold"))
    s.configure("Good.TLabel",  background=SURFACE, foreground=SUCCESS,
                font=("Segoe UI", 22, "bold"))
    s.configure("Bad.TLabel",   background=SURFACE, foreground=DANGER,
                font=("Segoe UI", 22, "bold"))

    s.configure("BigStat.TLabel", background=SURFACE, foreground=ACCENT, font=("Segoe UI", 28, "bold"))
    s.configure("BigWarn.TLabel", background=SURFACE, foreground=WARNING, font=("Segoe UI", 28, "bold"))
    s.configure("BigGood.TLabel", background=SURFACE, foreground=SUCCESS, font=("Segoe UI", 28, "bold"))
    s.configure("Total.TLabel",  background=SURFACE, foreground=SUCCESS, font=("Segoe UI", 18, "bold"))
    s.configure("Period.TLabel", background=SURFACE, foreground=MUTED,   font=("Segoe UI", 11))
    s.configure("RptStat.TLabel", background=SURFACE, foreground=ACCENT, font=("Segoe UI", 24, "bold"))

    s.configure("TNotebook",           background=BG, borderwidth=0, tabmargins=0)
    s.configure("TNotebook.Tab",       background=SURFACE2, foreground=MUTED,
                font=("Segoe UI", 10), padding=[18, 8], borderwidth=0)
    s.map("TNotebook.Tab",
          background=[("selected", SURFACE)],
          foreground=[("selected", TEXT)])

    s.configure("TEntry",       **{k: common[k] for k in
                 ("background", "foreground", "fieldbackground",
                  "bordercolor", "lightcolor", "darkcolor")},
                font=("Segoe UI", 10), padding=6, relief="flat")
    s.map("TEntry", fieldbackground=[("focus", FOCUS)])

    s.configure("TCombobox",    **{k: common[k] for k in
                 ("background", "foreground", "fieldbackground",
                  "bordercolor", "lightcolor", "darkcolor")},
                font=("Segoe UI", 10), padding=6)
    s.map("TCombobox", fieldbackground=[("readonly", SURFACE2)])

    s.configure("Treeview",     background=SURFACE2, foreground=TEXT,
                fieldbackground=SURFACE2, borderwidth=0, rowheight=28,
                font=("Segoe UI", 9))
    s.configure("Treeview.Heading", background=SURFACE, foreground=MUTED,
                borderwidth=0, font=("Segoe UI", 9, "bold"), relief="flat")
    s.map("Treeview", background=[("selected", ACCENT)],
          foreground=[("selected", "#FFFFFF")])

    s.configure("TScrollbar",   background=SURFACE2, troughcolor=SURFACE,
                borderwidth=0, arrowsize=12)

    s.configure("Primary.TButton", background=ACCENT,  foreground="#FFFFFF",
                font=("Segoe UI", 10, "bold"), padding=[16, 8], relief="flat",
                borderwidth=0)
    s.map("Primary.TButton", background=[("active", BTN_ACTIVE), ("pressed", BTN_PRESSED)])

    s.configure("Success.TButton", background=SUCCESS, foreground="#0F1117",
                font=("Segoe UI", 10, "bold"), padding=[16, 8], relief="flat",
                borderwidth=0)
    s.map("Success.TButton", background=[("active", SUCC_ACTIVE)])

    s.configure("Danger.TButton",  background=DANGER,  foreground="#FFFFFF",
                font=("Segoe UI", 10, "bold"), padding=[16, 8], relief="flat",
                borderwidth=0)
    s.map("Danger.TButton",  background=[("active", DANG_ACTIVE)])

    s.configure("TSpinbox",  background=SURFACE2, foreground=TEXT,
                fieldbackground=SURFACE2, bordercolor=BORDER,
                font=("Segoe UI", 10), arrowcolor=MUTED)


# ── Reusable widgets ───────────────────────────────────────────────────────────

def _card(parent, **kwargs) -> ttk.Frame:
    f = ttk.Frame(parent, style="Card.TFrame", padding=kwargs.pop("padding", 16))
    for k, v in kwargs.items():
        f.configure(**{k: v})
    return f


def _label(parent, text, style="Card.TLabel", **kw) -> ttk.Label:
    return ttk.Label(parent, text=text, style=style, **kw)


def _entry(parent, textvariable=None, width=22, **kw) -> ttk.Entry:
    return ttk.Entry(parent, textvariable=textvariable, width=width, **kw)


def _btn(parent, text, cmd, style="Primary.TButton", **kw) -> ttk.Button:
    return ttk.Button(parent, text=text, command=cmd, style=style, **kw)


def _tree(parent, cols, show="headings", height=12):
    tv = ttk.Treeview(parent, columns=cols, show=show, height=height)
    for c in cols:
        tv.heading(c, text=c)
        tv.column(c, anchor="center", minwidth=60, width=110)
    sb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    return tv, sb


# ══════════════════════════════════════════════════════════════════════════════
# TAB: Dashboard
# ══════════════════════════════════════════════════════════════════════════════

class DashboardTab(ttk.Frame):
    def __init__(self, master, inv: InventoryService, sales: SalesService):
        super().__init__(master, style="TFrame", padding=20)
        self._inv   = inv
        self._sales = sales
        self._build()

    def _build(self):
        _label(self, "📊  Dashboard", style="Head.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 16))

        self._cards = {}
        specs = [
            ("total_products", "Total Products",   "BigStat.TLabel"),
            ("low_stock",      "Low Stock Items",  "BigWarn.TLabel"),
            ("today_sales",    "Today's Sales",    "BigGood.TLabel"),
        ]
        for col, (key, title, style_name) in enumerate(specs):
            c = _card(self, padding=20)
            c.grid(row=1, column=col, sticky="nsew", padx=(0, 12 if col < 2 else 0))
            _label(c, title, style="Muted.TLabel").pack(anchor="w")
            lbl = ttk.Label(c, text="—", style=style_name)
            lbl.pack(anchor="w", pady=(4, 0))
            self._cards[key] = lbl

        self.columnconfigure((0, 1, 2), weight=1)

        # Recent products table
        c2 = _card(self, padding=16)
        c2.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(16, 0))
        _label(c2, "All Products", style="Head.TLabel").pack(anchor="w", pady=(0, 8))

        cols = ("ID", "Name", "Category", "Price ($)", "Cost ($)", "Stock")
        self._tv, sb = _tree(c2, cols, height=14)
        self._tv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.rowconfigure(2, weight=1)
        self.refresh()

    def apply_theme(self):
        self._tv.tag_configure("low", foreground=WARNING)

    def refresh(self):
        products = self._inv.list_all()
        low = sum(1 for p in products if p.stock < 5)

        now = datetime.now()
        try:
            rep = self._sales.monthly_report(now.year, now.month)
            today_inc = rep.income
        except Exception:
            today_inc = 0.0

        self._cards["total_products"].config(text=str(len(products)))
        self._cards["low_stock"].config(text=str(low))
        self._cards["today_sales"].config(text=f"${today_inc:,.2f}")

        for row in self._tv.get_children():
            self._tv.delete(row)
        for p in products:
            tag = "low" if p.stock < 5 else ""
            self._tv.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"${p.price:.2f}", f"${p.cost:.2f}", p.stock,
            ), tags=(tag,))
        self._tv.tag_configure("low", foreground=WARNING)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: Inventory (Add / Restock)
# ══════════════════════════════════════════════════════════════════════════════

CATEGORIES = ["Beverages", "Dairy", "Snacks", "Grains & Cereals",
               "Personal Care", "Household", "Frozen", "Produce", "Other"]


class InventoryTab(ttk.Frame):
    def __init__(self, master, inv: InventoryService, on_change):
        super().__init__(master, style="TFrame", padding=20)
        self._inv       = inv
        self._on_change = on_change
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        _label(self, "📦  Inventory Management", style="Head.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        # ── Add Product form ──────────────────────────────────────────────────
        form = _card(self, padding=20)
        form.grid(row=1, column=0, sticky="nsew", padx=(0, 12))

        _label(form, "Add New Product", style="Head.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self._vars = {k: tk.StringVar() for k in
                      ("name", "category", "price", "cost", "stock")}

        fields = [
            ("Product Name",  "name",     None),
            ("Category",      "category", CATEGORIES),
            ("Selling Price", "price",    None),
            ("Cost Price",    "cost",     None),
            ("Initial Stock", "stock",    None),
        ]
        for r, (lbl, key, opts) in enumerate(fields, start=1):
            _label(form, lbl, style="Muted.TLabel").grid(
                row=r, column=0, sticky="w", pady=4)
            if opts:
                w = ttk.Combobox(form, textvariable=self._vars[key],
                                 values=opts, state="readonly", width=20)
                w.current(0)
            else:
                w = _entry(form, textvariable=self._vars[key], width=22)
            w.grid(row=r, column=1, sticky="ew", padx=(8, 0), pady=4)
        form.columnconfigure(1, weight=1)

        _btn(form, "➕  Add Product", self._add_product).grid(
            row=len(fields)+1, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # ── Restock panel ─────────────────────────────────────────────────────
        rst = _card(self, padding=20)
        rst.grid(row=2, column=0, sticky="ew", padx=(0, 12), pady=(12, 0))

        _label(rst, "Restock Existing Product", style="Head.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self._rst_id  = tk.StringVar()
        self._rst_qty = tk.StringVar()

        _label(rst, "Product ID", style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", pady=4)
        _entry(rst, textvariable=self._rst_id, width=10).grid(
            row=1, column=1, sticky="ew", padx=(8, 0))

        _label(rst, "Qty to Add",  style="Muted.TLabel").grid(
            row=2, column=0, sticky="w", pady=4)
        _entry(rst, textvariable=self._rst_qty, width=10).grid(
            row=2, column=1, sticky="ew", padx=(8, 0))
        rst.columnconfigure(1, weight=1)

        _btn(rst, "🔄  Restock", self._restock, style="Success.TButton").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # ── Product table ─────────────────────────────────────────────────────
        right = _card(self, padding=16)
        right.grid(row=1, column=1, rowspan=2, sticky="nsew")
        _label(right, "Product Catalogue", style="Head.TLabel").pack(
            anchor="w", pady=(0, 8))

        cols = ("ID", "Name", "Category", "Price", "Cost", "Stock")
        self._tv, sb = _tree(right, cols, height=18)
        self._tv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self._tv.tag_configure("low", foreground=WARNING)

        self.refresh()

    def _add_product(self):
        try:
            p = ProductDTO(
                product_id=None,
                name=self._vars["name"].get().strip(),
                category=self._vars["category"].get(),
                price=float(self._vars["price"].get()),
                cost=float(self._vars["cost"].get()),
                stock=int(self._vars["stock"].get()),
            )
            self._inv.add_product(p)
            messagebox.showinfo("Success", f"Product '{p.name}' added.")
            for v in self._vars.values():
                v.set("")
            self.refresh()
            self._on_change()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _restock(self):
        try:
            pid = int(self._rst_id.get())
            qty = int(self._rst_qty.get())
            self._inv.restock(pid, qty)
            messagebox.showinfo("Restocked", f"Added {qty} units to product {pid}.")
            self._rst_id.set("")
            self._rst_qty.set("")
            self.refresh()
            self._on_change()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        for row in self._tv.get_children():
            self._tv.delete(row)
        for p in self._inv.list_all():
            tag = "low" if p.stock < 5 else ""
            self._tv.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"${p.price:.2f}", f"${p.cost:.2f}", p.stock,
            ), tags=(tag,))

    def apply_theme(self):
        self._tv.tag_configure("low", foreground=WARNING)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: Sales (Point of Sale)
# ══════════════════════════════════════════════════════════════════════════════

class SalesTab(ttk.Frame):
    def __init__(self, master, inv: InventoryService, sales: SalesService, on_change):
        super().__init__(master, style="TFrame", padding=20)
        self._inv       = inv
        self._sales     = sales
        self._on_change = on_change
        self._cart: list[SaleItemDTO] = []
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        _label(self, "🛒  Point of Sale", style="Head.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        # ── Add item to cart ──────────────────────────────────────────────────
        left = _card(self, padding=20)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        _label(left, "Add Item to Cart", style="Head.TLabel").pack(
            anchor="w", pady=(0, 10))

        self._pid = tk.StringVar()
        self._qty = tk.StringVar(value="1")

        row_f = ttk.Frame(left, style="Card.TFrame")
        row_f.pack(fill="x", pady=4)
        _label(row_f, "Product ID", style="Muted.TLabel").pack(side="left")
        _entry(row_f, textvariable=self._pid, width=10).pack(
            side="left", padx=(8, 0))

        row_q = ttk.Frame(left, style="Card.TFrame")
        row_q.pack(fill="x", pady=4)
        _label(row_q, "Quantity  ", style="Muted.TLabel").pack(side="left")
        _entry(row_q, textvariable=self._qty, width=10).pack(
            side="left", padx=(8, 0))

        _btn(left, "＋  Add to Cart", self._add_to_cart).pack(
            fill="x", pady=(10, 0))

        # Product quick-ref
        sep = ttk.Separator(left, orient="horizontal")
        sep.pack(fill="x", pady=14)
        _label(left, "Available Products", style="Muted.TLabel").pack(anchor="w")

        cols = ("ID", "Name", "Price", "Stock")
        self._ref_tv, ref_sb = _tree(left, cols, height=10)
        self._ref_tv.pack(side="left", fill="both", expand=True)
        ref_sb.pack(side="right", fill="y")
        self._ref_tv.bind("<ButtonRelease-1>", self._pick_product)

        # ── Cart + checkout ───────────────────────────────────────────────────
        right = _card(self, padding=20)
        right.grid(row=1, column=1, sticky="nsew")
        _label(right, "Current Cart", style="Head.TLabel").pack(
            anchor="w", pady=(0, 8))

        cols2 = ("Product", "Qty", "Unit Price", "Subtotal")
        self._cart_tv, cart_sb = _tree(right, cols2, height=12)
        self._cart_tv.pack(side="left", fill="both", expand=True)
        cart_sb.pack(side="right", fill="y")

        bottom = ttk.Frame(right, style="Card.TFrame")
        bottom.pack(fill="x", pady=(12, 0))

        _label(bottom, "Total:", style="Card.TLabel").pack(side="left")
        self._total_lbl = ttk.Label(bottom, text="$0.00", style="Total.TLabel")
        self._total_lbl.pack(side="left", padx=8)

        btn_row = ttk.Frame(right, style="Card.TFrame")
        btn_row.pack(fill="x", pady=(8, 0))
        _btn(btn_row, "🗑  Clear Cart",   self._clear_cart, style="Danger.TButton"
             ).pack(side="left", padx=(0, 8))
        _btn(btn_row, "✅  Confirm Sale", self._confirm_sale, style="Success.TButton"
             ).pack(side="left")

        self.refresh()

    def _add_to_cart(self):
        try:
            pid = int(self._pid.get())
            qty = int(self._qty.get())
            if qty <= 0:
                raise ValueError("Quantity must be positive.")
            p = self._inv.search_products(str(pid))
            p = next((x for x in p if x.product_id == pid), None)
            if not p:
                raise LookupError(f"Product {pid} not found.")
            # merge if already in cart
            for item in self._cart:
                if item.product_id == pid:
                    item.quantity += qty
                    self._update_cart_view()
                    return
            self._cart.append(SaleItemDTO(
                product_id=pid, product_name=p.name,
                quantity=qty, unit_price=p.price))
            self._update_cart_view()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _pick_product(self, _event):
        sel = self._ref_tv.selection()
        if sel:
            vals = self._ref_tv.item(sel[0], "values")
            self._pid.set(vals[0])

    def _update_cart_view(self):
        for row in self._cart_tv.get_children():
            self._cart_tv.delete(row)
        total = 0.0
        for item in self._cart:
            sub = item.subtotal
            total += sub
            self._cart_tv.insert("", "end", values=(
                item.product_name, item.quantity,
                f"${item.unit_price:.2f}", f"${sub:.2f}",
            ))
        self._total_lbl.config(text=f"${total:.2f}")

    def _clear_cart(self):
        self._cart.clear()
        self._update_cart_view()

    def _confirm_sale(self):
        if not self._cart:
            messagebox.showwarning("Empty Cart", "Add items before confirming.")
            return
        try:
            import copy
            items_copy = copy.deepcopy(self._cart)
            sale = self._sales.process_sale(items_copy)
            messagebox.showinfo(
                "Sale Complete",
                f"Sale #{sale.sale_id} recorded.\nTotal: ${sale.total:.2f}",
            )
            self._cart.clear()
            self._update_cart_view()
            self.refresh()
            self._on_change()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        for row in self._ref_tv.get_children():
            self._ref_tv.delete(row)
        for p in self._inv.list_all():
            self._ref_tv.insert("", "end", values=(
                p.product_id, p.name, f"${p.price:.2f}", p.stock,
            ))


# ══════════════════════════════════════════════════════════════════════════════
# TAB: Search
# ══════════════════════════════════════════════════════════════════════════════

class SearchTab(ttk.Frame):
    COL_MAP = {
        "ID":         "product_id",
        "Name":       "name",
        "Category":   "category",
        "Price ($)":  "price",
        "Cost ($)":   "cost",
        "Stock":      "stock",
    }

    def __init__(self, master, inv: InventoryService):
        super().__init__(master, style="TFrame", padding=20)
        self._inv = inv
        self._products: list = []
        self._sort_col: str | None = None
        self._sort_rev = False
        self._build()

    def _build(self):
        _label(self, "🔍  Search Products", style="Head.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 16))

        bar = _card(self, padding=12)
        bar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 12))

        self._term = tk.StringVar()
        _label(bar, "Search (Name / ID / Category):", style="Muted.TLabel"
               ).pack(side="left", padx=(0, 8))
        e = _entry(bar, textvariable=self._term, width=36)
        e.pack(side="left", padx=(0, 8))
        e.bind("<Return>", lambda _: self._search())
        _btn(bar, "Search", self._search).pack(side="left", padx=(0, 8))
        _btn(bar, "Show All", self._show_all, style="Success.TButton").pack(side="left")

        res = _card(self, padding=16)
        res.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        cols = tuple(self.COL_MAP.keys())
        self._tv, sb = _tree(res, cols, height=20)
        self._tv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for col in cols:
            self._tv.heading(col, command=lambda c=col: self._sort_by(c))
        self._show_all()

    def _sort_by(self, col):
        attr = self.COL_MAP[col]
        if self._sort_col == col:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_col = col
            self._sort_rev = False
        self._products.sort(key=lambda p: getattr(p, attr) or 0, reverse=self._sort_rev)
        self._populate(self._products)

    def _search(self):
        term = self._term.get().strip()
        self._products = self._inv.search_products(term) if term else self._inv.list_all()
        self._sort_col = None
        self._populate(self._products)

    def _show_all(self):
        self._term.set("")
        self._products = self._inv.list_all()
        self._sort_col = None
        self._populate(self._products)

    def _populate(self, products):
        for row in self._tv.get_children():
            self._tv.delete(row)
        for p in products:
            self._tv.insert("", "end", values=(
                p.product_id, p.name, p.category,
                f"${p.price:.2f}", f"${p.cost:.2f}", p.stock,
            ))


# ══════════════════════════════════════════════════════════════════════════════
# TAB: Reports
# ══════════════════════════════════════════════════════════════════════════════

class ReportsTab(ttk.Frame):
    def __init__(self, master, sales: SalesService):
        super().__init__(master, style="TFrame", padding=20)
        self._sales = sales
        self._build()

    def _build(self):
        _label(self, "📈  Income & Expense Reports", style="Head.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        # Controls
        ctrl = _card(self, padding=14)
        ctrl.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        now = datetime.now()

        _label(ctrl, "Year:", style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self._year = tk.StringVar(value=str(now.year))
        ttk.Spinbox(ctrl, from_=2000, to=2100, textvariable=self._year,
                    width=6, font=("Segoe UI", 10)).pack(side="left", padx=(0, 16))

        _label(ctrl, "Month (1–12):", style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self._month = tk.StringVar(value=str(now.month))
        ttk.Spinbox(ctrl, from_=1, to=12, textvariable=self._month,
                    width=4, font=("Segoe UI", 10)).pack(side="left", padx=(0, 16))

        _label(ctrl, "Week (1–53):", style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self._week = tk.StringVar(value=str(now.isocalendar()[1]))
        ttk.Spinbox(ctrl, from_=1, to=53, textvariable=self._week,
                    width=4, font=("Segoe UI", 10)).pack(side="left", padx=(0, 16))

        _btn(ctrl, "📅  Monthly Report", self._monthly).pack(side="left", padx=(0, 8))
        _btn(ctrl, "📆  Weekly Report",  self._weekly,  style="Success.TButton").pack(side="left")

        # Stat cards (3 columns)
        stats = _card(self, padding=16)
        stats.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        stats.columnconfigure((0, 1, 2, 3), weight=1)

        self._period_lbl = ttk.Label(stats, text="—", style="Period.TLabel")
        self._period_lbl.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        stat_defs = [
            ("income_lbl",  "Revenue",   "Stat.TLabel"),
            ("expense_lbl", "COGS",      "Stat.TLabel"),
            ("profit_lbl",  "Profit",    "Good.TLabel"),
            ("sales_lbl",   "# Sales",   "Stat.TLabel"),
        ]
        for col, (attr, title, style) in enumerate(stat_defs):
            sf = ttk.Frame(stats, style="Card.TFrame")
            sf.grid(row=1, column=col, sticky="nsew", padx=(0, 12 if col < 3 else 0))
            _label(sf, title, style="Muted.TLabel").pack(anchor="w")
            lbl = ttk.Label(sf, text="—", style="RptStat.TLabel")
            lbl.pack(anchor="w")
            setattr(self, f"_{attr}", lbl)

        # History log
        log = _card(self, padding=16)
        log.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        _label(log, "Report History", style="Head.TLabel").pack(anchor="w", pady=(0, 8))

        cols = ("Period", "Revenue ($)", "COGS ($)", "Profit ($)", "# Sales")
        self._tv, sb = _tree(log, cols, height=10)
        self._tv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self._tv.tag_configure("profit",  foreground=SUCCESS)
        self._tv.tag_configure("loss",    foreground=DANGER)

    def _monthly(self):
        try:
            r = self._sales.monthly_report(int(self._year.get()), int(self._month.get()))
            self._show(r)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _weekly(self):
        try:
            r = self._sales.weekly_report(int(self._year.get()), int(self._week.get()))
            self._show(r)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show(self, r):
        self._period_lbl.config(text=f"Period: {r.period_label}")
        self._income_lbl.config(text=f"${r.income:,.2f}")
        self._expense_lbl.config(text=f"${r.expense:,.2f}")

        color = SUCCESS if r.profit >= 0 else DANGER
        self._profit_lbl.config(text=f"${r.profit:,.2f}", foreground=color)
        self._sales_lbl.config(text=str(r.num_sales))

        tag = "profit" if r.profit >= 0 else "loss"
        self._tv.insert("", 0, values=(
            r.period_label,
            f"${r.income:,.2f}",
            f"${r.expense:,.2f}",
            f"${r.profit:,.2f}",
            r.num_sales,
        ), tags=(tag,))

    def apply_theme(self):
        self._tv.tag_configure("profit", foreground=SUCCESS)
        self._tv.tag_configure("loss", foreground=DANGER)


# ══════════════════════════════════════════════════════════════════════════════
# Main Application Window
# ══════════════════════════════════════════════════════════════════════════════

class MiniMartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛒  Mini Mart Management System")
        self.geometry("1200x760")
        self.minsize(960, 640)
        self.configure(bg=BG)

        _style(self)
        init_db()

        # Wire up DI
        p_repo  = ProductRepository()
        s_repo  = SaleRepository()
        self._inv   = InventoryService(p_repo)
        self._sales = SalesService(s_repo, p_repo)

        self._build_header()
        self._build_notebook()

    def _build_header(self):
        self._hdr = tk.Frame(self, bg=SURFACE, height=54)
        self._hdr.pack(fill="x", side="top")
        self._hdr.pack_propagate(False)

        self._title_lbl = tk.Label(self._hdr, text="🛒  Mini Mart Management System",
                                   bg=SURFACE, fg=TEXT,
                                   font=("Segoe UI", 14, "bold"))
        self._title_lbl.pack(side="left", padx=20, pady=12)

        self._clock_lbl = tk.Label(self._hdr, text="", bg=SURFACE, fg=MUTED,
                                   font=("Segoe UI", 10))
        self._clock_lbl.pack(side="right", padx=20)

        self._theme_btn = tk.Button(self._hdr, text="☀️  Light", bg=SURFACE2, fg=TEXT,
                                     font=("Segoe UI", 9), bd=0, padx=10, pady=2,
                                     cursor="hand2", activebackground=ACCENT,
                                     activeforeground="#FFFFFF",
                                     command=self._toggle_theme)
        self._theme_btn.pack(side="right", padx=(0, 8))

        self._tick()

    def _tick(self):
        self._clock_lbl.config(text=datetime.now().strftime("%a %d %b %Y  %H:%M:%S"))
        self.after(1000, self._tick)

    def _toggle_theme(self):
        new = "light" if _current_theme == "dark" else "dark"
        _set_theme(new)
        _style(self)
        self.configure(bg=BG)
        self._hdr.configure(bg=SURFACE)
        self._title_lbl.configure(bg=SURFACE, fg=TEXT)
        self._clock_lbl.configure(bg=SURFACE, fg=MUTED)
        icon = "🌙" if new == "dark" else "☀️"
        label = "  Dark" if new == "dark" else "  Light"
        self._theme_btn.config(text=icon + label, bg=SURFACE2, fg=TEXT,
                               activebackground=ACCENT)
        for tab in (self._dash, self._inv_tab, self._sale_tab, self._rpt_tab):
            if hasattr(tab, "apply_theme"):
                tab.apply_theme()

    def _build_notebook(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        self._dash = DashboardTab(nb, self._inv, self._sales)
        self._inv_tab  = InventoryTab(nb, self._inv, self._refresh_all)
        self._sale_tab = SalesTab(nb, self._inv, self._sales, self._refresh_all)
        self._srch_tab = SearchTab(nb, self._inv)
        self._rpt_tab  = ReportsTab(nb, self._sales)

        nb.add(self._dash,      text="  Dashboard  ")
        nb.add(self._inv_tab,   text="  Inventory  ")
        nb.add(self._sale_tab,  text="  Sales POS  ")
        nb.add(self._srch_tab,  text="  Search  ")
        nb.add(self._rpt_tab,   text="  Reports  ")

    def _refresh_all(self):
        self._dash.refresh()
        self._inv_tab.refresh()
        self._sale_tab.refresh()
