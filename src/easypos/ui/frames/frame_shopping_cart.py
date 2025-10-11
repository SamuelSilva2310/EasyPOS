
import customtkinter as ctk
from easypos.ui.components.shopping_cart_item import ShoppingCartItem
from easypos.settings import APP_SETTINGS
from easypos.utils import utils

import logging
logger = logging.getLogger(__name__)

class ShoppingCartFrame(ctk.CTkFrame):
    def __init__(self, parent, on_cart_change_callback=None):
        super().__init__(parent)


        self.on_cart_change_callback = on_cart_change_callback
        self.cart_items = {} # { item_id: {'item': item, 'quantity': X, 'widget': widget} }


        self._create_ui_components()
        

    # === UI ===
    def _create_ui_components(self):
        # === Title ===
        self.title_label = ctk.CTkLabel(
            self,
            text="Carrinho",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.title_label.pack(fill="x", padx=10, pady=(10, 5))

        # === Scrollable Items Frame ===
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, pady=(0, 0))

        # === Bottom Action Bar ===
        self.cart_action_frame = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.cart_action_frame.pack(fill="x", side="bottom", pady=(0, 0))

        # Grid layout inside the bottom bar
        self.cart_action_frame.columnconfigure(0, weight=1)

        # “Clear Cart” button on the right
        self.btn_clear_cart = ctk.CTkButton(
            self.cart_action_frame,
            text="Limpar carrinho",
            command=self.clear_cart,
            width=140,
            height=36,
            corner_radius=8,
        )
        


    def update_clear_button_visibility(self):
        """Show or hide the 'Clear Cart' button depending on cart contents."""
        if len(self.cart_items) > 0:
            # If it's not already visible, re-grid it
            if not self.btn_clear_cart.winfo_ismapped():
                self.btn_clear_cart.grid(row=0, column=0, sticky="e", padx=15, pady=10)
        else:
            # Hide the button
            self.btn_clear_cart.grid_forget()

    # === Logic ===
    def add_item(self, item):
        logger.info(f"Adding item to cart: {item.name}")
        if item.id in self.cart_items:
            self.cart_items[item.id]['quantity'] += 1
            self.cart_items[item.id]['widget'].increase_quantity()
        else:
            self.cart_items[item.id] = {'item': item, 'quantity': 1}
            widget = self._create_item_widget(item.id)
            self.cart_items[item.id]['widget'] = widget
        self._refresh()

    

    def remove_item(self, item_id):
        if item_id in self.cart_items:
            self._remove_item_widget(item_id)
            del self.cart_items[item_id]
        self._refresh()

    def clear_cart(self):
        for item_id in self.cart_items:
            self._remove_item_widget(item_id)
        self.cart_items = {}
        self._refresh()
                
    
    def _on_item_quantity_change(self, item, new_quantity):
        self.cart_items[item.id]['quantity'] = new_quantity
        logger.info(f"Item {item.id} quantity changed to {new_quantity}")
        logger.info("Cart items: {}".format(self.cart_items))
        self._refresh()

    def _on_item_remove(self, item):
        self.remove_item(item.id)

    def _create_item_widget(self, item_id):

        cart_item = self.cart_items[item_id]
        item = cart_item['item']
        quantity = cart_item['quantity']

        widget = ShoppingCartItem(self.scroll_frame, item, quantity, self._on_item_quantity_change, self._on_item_remove)
        widget.pack()

        return widget

    def _remove_item_widget(self, item_id):
        widget = self.cart_items[item_id]['widget']
        widget.destroy()

    

    def _refresh(self):
        logger.info("Refreshing cart...")
        self.update_clear_button_visibility()
        if self.on_cart_change_callback:
            self.on_cart_change_callback(self.cart_items)
