import customtkinter as ctk
import os
from PIL import Image
from easypos.ui.styles import UISettings
from easypos.ui.components.hover_button import HoverButton

BUTTON_WIDTH = 90
BUTTON_HEIGHT = 70
IMAGE_SCALE_FACTOR = 0.8


class CategoriesFrame(ctk.CTkFrame):
    """A compact, horizontally scrollable list of category buttons."""

    def __init__(self, parent, categories, on_category_select=None):
        super().__init__(parent)
        self.categories = categories or []
        self.on_category_select = on_category_select
        self.selected_category = None
        self.buttons = {}
        self.button_images = {}
        self.buttons_frame = None

        self._style()
        self._create_header("Categorias")
        self._create_buttons()

    # -------------------------------
    # UI Setup
    # -------------------------------

    def _style(self):
        """Base frame style."""
        self.configure(fg_color="transparent", border_width=0, corner_radius=0)

    def _create_header(self, title):
        """Create section title."""
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=UISettings.COLORS.get("primary_text", "white"),
        )
        title_label.pack(anchor="w", padx=10, pady=(UISettings.SPACING["medium"], 2))

    def _clear_buttons(self):
        """Destroy existing buttons frame and its buttons."""
        if self.buttons_frame:
            self.buttons_frame.destroy()
            self.buttons_frame = None
        self.buttons.clear()
        self.button_images.clear()

    def _create_buttons(self):
        """Create horizontally scrollable category buttons with compact height."""
        # Create scroll frame with fixed height matching buttons
        if self.buttons_frame:
            self._clear_buttons()
        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=BUTTON_HEIGHT + 20,  # Tight height fit
        )
        self.buttons_frame.pack(fill="x", expand=False, padx=5, pady=(0, UISettings.SPACING["small"]))

        padding_x = UISettings.SPACING.get("small", 6)
        padding_y = UISettings.SPACING.get("small", 6)
        col = 0


        # ---- "All" Button ----
        btn_all = HoverButton(
            parent=self.buttons_frame,
            text="Todos",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
        )
        btn_all.grid(row=0, column=col, padx=padding_x, pady=padding_y)
        btn_all.configure(command=lambda: self._on_select(None))
        self.buttons["all"] = btn_all
        col += 1

        # ---- Category Buttons ----
        for cat in self.categories:
            photo = self._load_icon(cat.icon)

            btn = HoverButton(
                parent=self.buttons_frame,
                text=cat.label,
                image=photo,
                compound="top",
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                corner_radius=10,
            )
            btn.grid(row=0, column=col, padx=padding_x, pady=2, sticky="n")
            btn.configure(command=lambda c=cat: self._on_select(c))
            self.buttons[cat.id] = btn
            col += 1

        # Ensure the scroll frame doesn't expand vertically
        #self.scroll_frame.grid_propagate(False)
    def refresh(self, categories):
        self.categories = categories
        self._create_buttons()
    # -------------------------------
    # Helpers
    # -------------------------------

    def _load_icon(self, icon_filename):
        """Safely load and resize category icon."""
        if not icon_filename:
            return None
        img_path = os.path.join("images", icon_filename)
        if not os.path.exists(img_path):
            return None

        img = Image.open(img_path)
        new_size = (
            int(BUTTON_WIDTH * IMAGE_SCALE_FACTOR),
            int(BUTTON_HEIGHT * IMAGE_SCALE_FACTOR),
        )
        photo = ctk.CTkImage(img, size=new_size)
        self.button_images[icon_filename] = photo  # keep reference alive
        return photo

    # -------------------------------
    # Interactivity
    # -------------------------------

    def _on_select(self, category):
        """Handle selection and highlight."""
        # Reset previous selection highlight
        if self.selected_category:
            prev_btn = self.buttons.get(self.selected_category.id if self.selected_category else "all")
            # if prev_btn:
            #     prev_btn.configure(fg_color=prev_btn.default_fg_color)

        # Highlight new selection
        self.selected_category = category
        btn = self.buttons.get(category.id if category else "all")
        if btn:
            btn.configure(fg_color=UISettings.COLORS["secondary"])

        # Call callback
        if self.on_category_select:
            self.on_category_select(category)