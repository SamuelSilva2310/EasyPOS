import tkinter as tk
from PIL import Image, ImageTk
import os

class ActionsFrame(tk.Frame):
    def __init__(self, parent, button_width=120, button_height=80):
        super().__init__(parent)
        self.item = None
        self.button_width = button_width
        self.button_height = button_height

        # Components
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
        self.icon_label = tk.Label(self)
        self.icon_label.grid(row=0, column=0, columnspan=2, pady=5)

        # Item title
        self.title_label = tk.Label(self, text="Select an item", font=("Arial", 16, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Quantity
        tk.Label(self, text="Quantity:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.input_quantity = tk.Entry(self)
        self.input_quantity.grid(row=2, column=1, padx=5, pady=5)
        self.input_quantity.insert(0, "1")

        # Item price
        tk.Label(self, text="Price:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.label_item_price = tk.Label(self, text="$0.00")
        self.label_item_price.grid(row=3, column=1, padx=5, pady=5)

        # Total price
        tk.Label(self, text="Total:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.label_total_price = tk.Label(self, text="$0.00")
        self.label_total_price.grid(row=4, column=1, padx=5, pady=5)

        # Money handed
        tk.Label(self, text="Money given:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.input_money_handed = tk.Entry(self)
        self.input_money_handed.grid(row=5, column=1, padx=5, pady=5)

        # Change
        tk.Label(self, text="Change:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.label_change = tk.Label(self, text="$0.00")
        self.label_change.grid(row=6, column=1, padx=5, pady=5)

        # Sell button
        self.button_sell = tk.Button(self, text="Sell", bg="lightgreen", command=self.sell)
        self.button_sell.grid(row=7, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    def update_ui(self, item):
        """Call this when an item is selected on the left frame."""
        self.item = item
        self.title_label.config(text=item.name)
        self.label_item_price.config(text=f"${item.price:.2f}")
        self.label_total_price.config(text=f"${item.price:.2f}")
        self.input_quantity.delete(0, tk.END)
        self.input_quantity.insert(0, "1")
        self.input_money_handed.delete(0, tk.END)
        self.label_change.config(text="$0.00")

        # Show icon if available
        image_path = os.path.join("images", item.icon)
        if hasattr(item, "icon") and item.icon and os.path.exists(image_path):
            img = Image.open(image_path).resize((50, 50))
            photo = ImageTk.PhotoImage(img)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo  # keep reference
        else:
            self.icon_label.config(image="", text="")

    def sell(self):
        """Handle selling the selected item."""
        if not self.item:
            tk.messagebox.showwarning("No Item", "Please select an item first.")
            return

        # Quantity
        try:
            quantity = int(self.input_quantity.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Invalid quantity", "Please enter a valid quantity.")
            return

        # Total
        total_price = self.item.price * quantity
        self.label_total_price.config(text=f"${total_price:.2f}")

        # Money given
        try:
            money_given = float(self.input_money_handed.get())
        except ValueError:
            money_given = 0.0

        # Change
        change = money_given - total_price
        self.label_change.config(text=f"${max(change,0):.2f}")

        # Log / trigger sale
        print(f"Sold {quantity} x {self.item.name} | Total: ${total_price:.2f} | Change: ${change:.2f}")

        # Here you could push the ticket to a queue for printing
        # ticket_queue.put(TicketModel(...))