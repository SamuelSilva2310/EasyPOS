import customtkinter as ctk
from easypos.ui.settings import UISettings
from easypos.ui.layout_left import LayoutLeft
from easypos.ui.layout_right import LayoutRight
from easypos.ui.settings import UISettings

from easypos.controllers.item import ItemController
from easypos.controllers.sale import SaleController

# Set global theme for CTk
UISettings.apply_theme()

class UIApp(ctk.CTk):

    def __init__(self, items, sale_controller):
        super().__init__()
        self.title("EasyPOS")
        self.geometry(UISettings.APP_WINDOW_SIZE)

        self.sale_controller = sale_controller
        
        self.leftFrame = None
        self.rightFrame = None 
        
        self.items = items

        self.create_top_bar()
        # create a sample button
        self._configure_layout()

    def create_top_bar(self):
        # --- Top bar frame ---
        top_bar = ctk.CTkFrame(self, height=60, fg_color="#2C3E50")
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        # --- Inner container for padding ---
        inner_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        inner_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=UISettings.SPACING["medium"], pady=8)
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=0)

        # --- Left: dropdown menu ---
        menu = ctk.CTkOptionMenu(inner_frame, values=["Menu 1", "Menu 2", "Menu 3"])
        menu.grid(row=0, column=0, sticky="w")

        # --- Right: settings button ---
        btn_settings = ctk.CTkButton(inner_frame, text="Settings", width=90, height=30)
        btn_settings.grid(row=0, column=1, sticky="e")

        # Optional: add subtle separation below top bar
        separator = ctk.CTkFrame(self, height=2, fg_color="#34495E")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew")
            



    def _configure_layout(self):
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)  # left side takes 2 parts
        self.grid_columnconfigure(1, weight=1)  # right side takes 1 part

        # Left frame
        self.leftFrame = LayoutLeft(self, self.items, self._on_item_selected)
        
        #self.leftFrame.configure(fg_color="#1E90FF")  # lightblue equivalent
        self.leftFrame.grid(row=1, column=0, sticky="nsew")

        # Right frame
        self.rightFrame = LayoutRight(parent=self, sale_controller=self.sale_controller)
        #self.rightFrame.configure(fg_color="#90EE90")  # lightgreen equivalent
        self.rightFrame.grid(row=1, column=1, sticky="nsew")
    
    def _on_item_selected(self, item):
        self.rightFrame.item_selected(item)
        print(f"Item selected: {item.name}")

    def run(self):
        self.mainloop()