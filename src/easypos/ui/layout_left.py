
import customtkinter as ctk
from easypos.ui.frames.frame_items import ItemsFrame

class LayoutLeft(ctk.CTkFrame):
    def __init__(self, parent, items, select_callback=None):
        super().__init__(parent)
        # Optional: add a label/title for the panel
        ctk.CTkLabel(self, text="Items", fg_color="lightblue", font=("Arial", 16)).pack(pady=5)

        # Add ItemsFrame
        self.items_frame = ItemsFrame(self, items, select_callback)
        #self.items_frame.config(bg="#4a90e2")
        self.items_frame.pack(fill="both", expand=True)