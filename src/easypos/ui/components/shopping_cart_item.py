import customtkinter as ctk
from easypos.utils import utils
from easypos.settings import APP_SETTINGS
import os
ICON_SIZE = (40, 40)


class ShoppingCartItem(ctk.CTkFrame):
    def __init__(self, parent, item, quantity, on_quantity_change=None, on_remove=None):
        super().__init__(parent, corner_radius=8, fg_color="transparent")

        self.item = item
        self.quantity_variable = ctk.StringVar(value=str(quantity))
        self.on_quantity_change = on_quantity_change  # callback to notify parent
        self.on_remove = on_remove

        self._create_ui_component()

    def _create_ui_component(self):
        """Builds a single cart row: image | name | - qty + | total"""
        
        # === Grid configuration ===
        self.grid_columnconfigure(0, weight=0)  # image
        self.grid_columnconfigure(1, weight=1)  # name
        self.grid_columnconfigure(2, weight=0)  # quantity controls
        self.grid_columnconfigure(3, weight=0)  # price
        self.grid_columnconfigure(4, weight=0)  # remove

        # === Item Image ===
        self.image = None
        if getattr(self.item, "icon", None):
            try:
                image_path = os.path.join(APP_SETTINGS.get("images_directory"), "products", self.item.icon)
                image = utils.load_image(image_path)
                self.image = ctk.CTkImage(image, size=ICON_SIZE)
            except Exception:
                pass

        self.label_image = ctk.CTkLabel(self, image=self.image, text="")
        self.label_image.grid(row=0, column=0, padx=(8, 10), pady=5, sticky="w")

        # === Item Name ===
        self.label_name = ctk.CTkLabel(
            self,
            text=self.item.name,
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,  # fixed width ensures alignment
        )
        self.label_name.grid(row=0, column=1, sticky="w", padx=(0, 10))

        # === Quantity Controls ===
        quantity_frame = ctk.CTkFrame(self, fg_color="transparent")
        quantity_frame.grid(row=0, column=2, padx=(5, 10), sticky="e")

        self.btn_minus = ctk.CTkButton(
            quantity_frame, text="–", width=25, command=self.decrease_quantity
        )
        self.btn_minus.pack(side="left", padx=2)

        self.input_quantity = ctk.CTkEntry(
            quantity_frame,
            textvariable=self.quantity_variable,
            width=40,
            justify="center"
        )
        self.input_quantity.pack(side="left")
        self.quantity_variable.trace_add("write", self._on_quantity_input_change)

        self.btn_plus = ctk.CTkButton(
            quantity_frame, text="+", width=25, command=self.increase_quantity
        )
        self.btn_plus.pack(side="left", padx=2)

        # === Total Price ===
        self.label_price = ctk.CTkLabel(
            self,
            text=f"{self.item.price * self._get_quantity():.2f} €",
            anchor="e",
            font=ctk.CTkFont(size=14),
            width=80
        )
        self.label_price.grid(row=0, column=3, padx=(10, 10), sticky="e")

        self.btn_remove = ctk.CTkButton(
            self, text="X", width=25, command=self._remove_item
        )
        self.btn_remove.grid(row=0, column=4, padx=(10, 10), sticky="e")

    # ------------------ BUTTON LOGIC ------------------ #

    def _remove_item(self):
        if self.on_remove:
            self.on_remove(self.item)

    def _get_quantity(self):
        """Safely read current quantity."""
        try:
            return int(self.quantity_variable.get() or 0)
        except ValueError:
            return 0

    def increase_quantity(self):
        """Increase quantity by 1."""
        new_value = self._get_quantity() + 1
        self.quantity_variable.set(str(new_value))
        self._update_display()

    def decrease_quantity(self):
        """Decrease quantity by 1, down to zero."""
        new_value = max(0, self._get_quantity() - 1)
        self.quantity_variable.set(str(new_value)) 
        self._update_display()

    def _on_quantity_input_change(self, *args):
        """Triggered when user types manually."""
        self._update_display()

    def _update_display(self):
        """Update price and notify parent of changes."""
        self.label_price.configure(
            text=f"{self.item.price * self._get_quantity():.2f} €"
        )
        if self.on_quantity_change:
            self.on_quantity_change(self.item, self._get_quantity())