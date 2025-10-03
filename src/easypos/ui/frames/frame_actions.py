import customtkinter as ctk
from PIL import Image, ImageTk
import os
import logging

logger = logging.getLogger(__name__)

class ActionsFrame(ctk.CTkFrame):
    def __init__(self, parent, sale_controller, button_width=120, button_height=80):
        super().__init__(parent)
        self.sale_controller = sale_controller

        self.item = None
        self.button_width = button_width
        self.button_height = button_height

        # State variables
        self.quantity_var = ctk.StringVar(value="1")
        self.money_var = ctk.StringVar(value="")

        # Widgets
        self.icon_label = None
        self.title_label = None
        self.input_quantity = None
        self.label_item_price = None
        self.label_total_price = None
        self.input_money_handed = None
        self.label_change = None
        self.button_sell = None

        self._create_components()

    def _create_components(self):
        # Icon placeholder
        self.icon_label = ctk.CTkLabel(self, text="", width=50, height=50)
        self.icon_label.grid(row=0, column=0, columnspan=2, pady=5)

        # Item title
        self.title_label = ctk.CTkLabel(self, text="Select an item", font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Quantity
        ctk.CTkLabel(self, text="Quantity:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.input_quantity = ctk.CTkEntry(self, textvariable=self.quantity_var)
        self.input_quantity.grid(row=2, column=1, padx=5, pady=5)

        # Item price
        ctk.CTkLabel(self, text="Price:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.label_item_price = ctk.CTkLabel(self, text="$0.00")
        self.label_item_price.grid(row=3, column=1, padx=5, pady=5)

        # Total price
        ctk.CTkLabel(self, text="Total:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.label_total_price = ctk.CTkLabel(self, text="$0.00")
        self.label_total_price.grid(row=4, column=1, padx=5, pady=5)

        # Money handed
        ctk.CTkLabel(self, text="Money given:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.input_money_handed = ctk.CTkEntry(self, textvariable=self.money_var)
        self.input_money_handed.grid(row=5, column=1, padx=5, pady=5)

        # Change
        ctk.CTkLabel(self, text="Change:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.label_change = ctk.CTkLabel(self, text="$0.00")
        self.label_change.grid(row=6, column=1, padx=5, pady=5)

        # Sell button
        self.button_sell = ctk.CTkButton(self, text="Sell", fg_color="lightgreen", command=self.sell)
        self.button_sell.grid(row=7, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

        # Bind changes
        self.quantity_var.trace_add("write", self._on_change)
        self.money_var.trace_add("write", self._on_change)

    def update_ui(self, item):
        """Call this when an item is selected on the left frame."""
        self.item = item
        self.title_label.configure(text=item.name)

        # Reset values
        self.quantity_var.set("1")
        self.money_var.set("")
        self.label_item_price.configure(text=f"${item.price:.2f}")
        self.label_total_price.configure(text=f"${item.price:.2f}")
        self.label_change.configure(text="$0.00")

        # Show icon if available
        image_path = os.path.join("images", getattr(item, "icon", ""))
        if hasattr(item, "icon") and item.icon and os.path.exists(image_path):
            img = Image.open(image_path).resize((50, 50))
            photo = ImageTk.PhotoImage(img)
            self.icon_label.configure(image=photo, text="")
            self.icon_label.image = photo  # keep reference
        else:
            self.icon_label.configure(image="", text="")

    def _on_change(self, *args):
        """Recalculate totals when quantity or money changes."""
        if not self.item:
            return

        # Quantity
        try:
            quantity = int(self.quantity_var.get())
            if quantity < 0:
                quantity = 0
        except ValueError:
            quantity = 0

        # Total
        total = self.item.price * quantity
        self.label_total_price.configure(text=f"${total:.2f}")

        # Money
        try:
            money = float(self.money_var.get())
        except ValueError:
            money = 0.0

        # Change
        change = money - total
        self.label_change.configure(text=f"${change:.2f}")

    def sell(self):
        """Handle selling the selected item."""
        if not self.item:
            ctk.CTkMessagebox.show_warning("No Item", "Please select an item first.")
            return

        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            ctk.CTkMessagebox.show_error("Invalid quantity", "Please enter a valid quantity.")
            return

        logger.info(f"Selling {quantity} of {self.item.name}")
        self.sale_controller.make_sale(self.item.id, quantity)