
import tkinter as tk
from easypos.ui.frames.frame_items import ItemsFrame

class LayoutLeft(tk.Frame):
    def __init__(self, parent, items, select_callback=None):
        super().__init__(parent)
        # Optional: add a label/title for the panel
        tk.Label(self, text="Items", bg="lightblue", font=("Arial", 16)).pack(pady=5)

        # Add ItemsFrame
        self.items_frame = ItemsFrame(self, items, select_callback)
        self.items_frame.config(bg="#4a90e2")
        self.items_frame.pack(fill="both", expand=True)