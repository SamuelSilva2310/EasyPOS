
import tkinter as tk
from easypos.ui.layout_left import LayoutLeft
from easypos.ui.layout_right import LayoutRight

from easypos.controllers.item import ItemController
from easypos.controllers.sale import SaleController

class UIApp(tk.Tk):

    def __init__(self, items):
        super().__init__()
        self.title("EasyPOS")
        self.geometry("800x600")


        self.leftFrame = None
        self.rightFrame = None 
        
        self.items = items
        self._configure_layout()


        
        

    def _configure_layout(self):
        
        # Configure grid weights (this is key!)
        self.grid_rowconfigure(0, weight=1)   # row stretches
        self.grid_columnconfigure(0, weight=2)  # left side takes 2 parts
        self.grid_columnconfigure(1, weight=1)  # right side takes 1 part

        self.leftFrame = LayoutLeft(self, self.items, self._on_item_selected)
        self.leftFrame.config(bg="lightblue")
        self.leftFrame.grid(row=0, column=0, sticky="nsew")

        self.rightFrame = LayoutRight(self)
        self.rightFrame.config(bg="lightgreen")
        self.rightFrame.grid(row=0, column=1, sticky="nsew")
    

    def _on_item_selected(self, item):
        self.rightFrame.item_selected(item)
        print(f"Item selected: {item.name}")

    def run(self):
        self.mainloop()