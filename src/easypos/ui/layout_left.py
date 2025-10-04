
import customtkinter as ctk
from easypos.ui.frames.frame_items import ItemsFrame
from easypos.ui.settings import UISettings

class LayoutLeft(ctk.CTkFrame):
    def __init__(self, parent, items, select_callback=None):
        super().__init__(parent)

        #self._configure()
        # Optional: add a label/title for the panel
        title = ctk.CTkLabel(self, text="Artigos", fg_color="transparent")
        title.pack(pady=UISettings.SPACING.get("medium"))

        self.configure(border_width=1, corner_radius=0)
        UISettings.style_title(title, primary=True)

        # Add ItemsFrame
        self.items_frame = ItemsFrame(self, items, select_callback)
        #self.items_frame.configure(fg_color=UISettings.COLORS["primary"])
        #self.items_frame.config(bg="#4a90e2")
        self.items_frame.pack(fill="both", expand=True)
    
    # def _configure(self):
    #     self.configure(fg_color=UISettings.COLORS["primary"])