import customtkinter as ctk

from easypos.ui.layout_left import LayoutLeft
from easypos.ui.layout_right import LayoutRight

from easypos.controllers.item import ItemController
from easypos.controllers.sale import SaleController

# Set global theme for CTk
ctk.set_default_color_theme("green")  # or "green", "dark-blue"
ctk.set_appearance_mode("dark")  # or "light"

class UIApp(ctk.CTk):

    def __init__(self, items, sale_controller):
        super().__init__()
        self.title("EasyPOS")
        self.geometry("800x600")

        self.sale_controller = sale_controller
        
        self.leftFrame = None
        self.rightFrame = None 
        
        self.items = items
        self._configure_layout()

    def _configure_layout(self):
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)  # left side takes 2 parts
        self.grid_columnconfigure(1, weight=1)  # right side takes 1 part

        # Left frame
        self.leftFrame = LayoutLeft(self, self.items, self._on_item_selected)
        
        #self.leftFrame.configure(fg_color="#1E90FF")  # lightblue equivalent
        self.leftFrame.grid(row=0, column=0, sticky="nsew")

        # Right frame
        self.rightFrame = LayoutRight(parent=self, sale_controller=self.sale_controller)
        #self.rightFrame.configure(fg_color="#90EE90")  # lightgreen equivalent
        self.rightFrame.grid(row=0, column=1, sticky="nsew")
    
    def _on_item_selected(self, item):
        self.rightFrame.item_selected(item)
        print(f"Item selected: {item.name}")

    def run(self):
        self.mainloop()