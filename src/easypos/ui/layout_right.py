
import customtkinter as ctk
from easypos.ui.frames.frame_actions import ActionsFrame
from easypos.ui.settings import UISettings

class LayoutRight(ctk.CTkFrame):
    def __init__(self, parent, sale_controller):
        super().__init__(parent)
        
        title = ctk.CTkLabel(self, text="Ações")
        title.pack(pady=UISettings.SPACING.get("medium"))
        UISettings.style_title(title, primary=True)


        # Add ActionsFrame
        self.actions_frame = ActionsFrame(self, sale_controller)
        #self.actions_frame.config(bg="#50e3c2")      # or self.cget("bg")
        self.actions_frame.pack(fill="both", expand=True)

    def item_selected(self, item):

        self.actions_frame.update_ui(item)
