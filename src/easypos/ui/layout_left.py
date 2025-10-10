
import customtkinter as ctk
from easypos.ui.frames.frame_items import ItemsFrame
from easypos.ui.frames.frame_categories import CategoriesFrame
from easypos.ui.settings import UISettings

from easypos.models.category import CategoryService
from easypos.models.item import ItemService

class LayoutLeft(ctk.CTkFrame):
    def __init__(self, parent, select_callback=None):
        super().__init__(parent)

        #self._configure()
        # Optional: add a label/title for the panel
        

        # title = ctk.CTkLabel(self, text="Artigos", fg_color="transparent")
        # title.pack(pady=UISettings.SPACING.get("medium"))

        # self.configure(border_width=0, corner_radius=0)
        # UISettings.style_title(title, primary=True)

        self.categories = CategoryService.get_all()
        self.categories_frame = CategoriesFrame(self, self.categories, on_category_select=self._on_category_select)
        self.categories_frame.pack(fill="x", expand=False)
        self.categories_frame.configure(height= 50 + 20)
        
        
        
        
        # Add ItemsFrame
        self.items = ItemService.get_items()
        self.items_frame = ItemsFrame(self, self.items, select_callback)
        #self.items_frame.configure(fg_color=UISettings.COLORS["primary"])
        #self.items_frame.config(bg="#4a90e2")
        self.items_frame.pack(fill="both", expand=True)
    
    def refresh_all(self):
        self.categories = CategoryService.get_all()
        self.items = ItemService.get_items()
        self.items_frame.refresh(self.items)
        self.categories_frame.refresh(self.categories)

    def _on_category_select(self, category):
        self.items_frame.filter_by_category(category)

    def refresh(self):
        self.items_frame.refresh()

    # def _configure(self):
    #     self.configure(fg_color=UISettings.COLORS["primary"])