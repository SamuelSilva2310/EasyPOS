
import customtkinter as ctk
from easypos.ui.frames.frame_actions import ActionsFrame
from easypos.ui.frames.frame_shopping_cart import ShoppingCartFrame
from easypos.ui.settings import UISettings

class LayoutRight(ctk.CTkFrame):
    def __init__(self, parent, sale_controller):
        super().__init__(parent)
        
        title = ctk.CTkLabel(self, text="Ações")
        title.pack(pady=UISettings.SPACING.get("medium"))
        UISettings.style_title(title, primary=True)


        # Add ActionsFrame
        self.shopping_cart_frame = ShoppingCartFrame(self, self._on_cart_change)
        self.shopping_cart_frame.pack(fill="both", expand=True)

        self.actions_frame = ActionsFrame(self, sale_controller, on_sale_complete=self._on_sale_complete)
        #self.actions_frame.config(bg="#50e3c2")      # or self.cget("bg")
        self.actions_frame.pack(fill="both", expand=True)


    def item_selected(self, item):
        """
        Called when an item is selected in the ItemsFrame.
        
        :param item: The selected item
        """
        self.shopping_cart_frame.add_item(item)
        

    def _on_cart_change(self, cart_items):
        print("Cart changed")
        self.actions_frame.update_ui(cart_items)
    
    def _on_sale_complete(self):
        self.shopping_cart_frame.clear_cart()