import customtkinter as ctk
from PIL import Image, ImageTk
import logging
from easypos.ui.settings import UISettings

logger = logging.getLogger(__name__)

class ActionsFrame(ctk.CTkFrame):
    def __init__(self, parent, sale_controller, on_sale_complete=None):
        super().__init__(parent)
        self.sale_controller = sale_controller
        self.on_sale_complete = on_sale_complete
        self.cart_items = {}

        # State variables
        self.money_var = ctk.StringVar(value="")
        self.total_price_var = ctk.StringVar(value="0.00 €")
        self.change_var = ctk.StringVar(value="0.00 €")

        # Layout configuration
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._create_components()

    def _create_components(self):
        padding_y = 10
        padding_x = 12

        # --- TOTAL SECTION ---
        total_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#F0F0F0", "#2b2b2b"))
        total_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=padding_x, pady=(padding_y, 4))

        total_frame.grid_columnconfigure(0, weight=1)
        total_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            total_frame, text="Total:", font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="e", padx=padding_x, pady=padding_y)

        self.label_total_price = ctk.CTkLabel(
            total_frame,
            textvariable=self.total_price_var,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#007700", "#66ff66"),
        )
        self.label_total_price.grid(row=0, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # --- PAYMENT SECTION ---
        payment_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#F0F0F0", "#2b2b2b"))
        payment_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=padding_x, pady=padding_y)

        payment_frame.grid_columnconfigure(0, weight=1)
        payment_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            payment_frame,
            text="Dinheiro recebido:",
            font=ctk.CTkFont(size=16),
        ).grid(row=0, column=0, sticky="e", padx=padding_x, pady=padding_y)

        self.input_money_handed = ctk.CTkEntry(
            payment_frame,
            textvariable=self.money_var,
            width=160,
            height=36,
            font=ctk.CTkFont(size=16)
        )
        self.input_money_handed.grid(row=0, column=1, sticky="w", padx=padding_x, pady=padding_y)

        ctk.CTkLabel(
            payment_frame,
            text="Troco:",
            font=ctk.CTkFont(size=16),
        ).grid(row=1, column=0, sticky="e", padx=padding_x, pady=padding_y)

        self.label_change = ctk.CTkLabel(
            payment_frame,
            textvariable=self.change_var,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0066cc", "#66b2ff"),
        )
        self.label_change.grid(row=1, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # --- SELL BUTTON ---
        self.button_sell = ctk.CTkButton(
            self,
            text="Vender",
            command=self.sell,
            height=48,
            width=220,
            corner_radius=10,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#007bff", "#1e90ff"),
            hover_color=("#0056b3", "#0077cc"),
        )
        self.button_sell.grid(row=2, column=0, columnspan=2, pady=(padding_y * 2, padding_y))

        # Trace entry changes
        self.money_var.trace_add("write", self._on_money_change)

    # ---------------- LOGIC ---------------- #

    def update_ui(self, cart_items):
        """Update total when cart changes."""
        self.cart_items = cart_items
        total = 0.0
        for data in cart_items.values():
            item = data["item"]
            quantity = data["quantity"]
            total += item.price * quantity

        self.total_price_var.set(f"{total:.2f} €")
        self._on_money_change()  # update change immediately

    def _on_money_change(self, *args):
        """Recalculate change dynamically."""
        try:
            total_str = self.total_price_var.get().replace("€", "").strip()
            total = float(total_str) if total_str else 0.0
        except ValueError:
            total = 0.0

        try:
            money = float(self.money_var.get().replace(",", "."))
        except ValueError:
            money = 0.0

        change = money - total
        self.change_var.set(f"{change:.2f} €")

    def sell(self):
        """Finalize the sale for all items in cart."""
        logger.info("Processing sale for cart...")
        self.sale_controller.make_sale(self.cart_items)
        if self.on_sale_complete:
            self.on_sale_complete()