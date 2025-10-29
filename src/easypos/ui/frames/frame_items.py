import customtkinter as ctk
import os
from PIL import Image
from easypos.ui.styles import UISettings
from easypos.ui.components.hover_button import HoverButton
import logging
from easypos.settings import APP_SETTINGS
from easypos.utils import utils

logger = logging.getLogger(__name__)

BUTTON_GRID_COLS = 3
IMAGE_SCALE_FACTOR = 0.5
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 120


class ItemsFrame(ctk.CTkScrollableFrame):
    """Scrollable frame displaying items as buttons with icons and filtering."""

    def __init__(self, parent, items, select_callback=None):
        super().__init__(parent)

        # Full list of items
        self._all_items = items or []
        self.items = list(self._all_items)  # Current visible items
        self.select_callback = select_callback
        self.selected_item = None

        self.buttons = {}
        self.buttons_frame = None

        self._style()
        self._create_header("Artigos")
        self._create_buttons_grid(self.items)

    # -------------------------------
    # UI Setup
    # -------------------------------


    def _style(self):
        self.configure(border_width=0, corner_radius=0, fg_color="transparent")

    def _create_header(self, title):
        """Create title label for the section."""
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(UISettings.SPACING["medium"], 5))

        label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        label.pack(side="left", padx=10, anchor="w")

    def refresh(self, items):
        self.items = items
        self._create_buttons_grid(self.items)

    # -------------------------------
    # Button Grid
    # -------------------------------

    def _clear_buttons(self):
        """Destroy existing buttons frame and its buttons."""
        if self.buttons_frame:
            self.buttons_frame.destroy()
            self.buttons_frame = None
        self.buttons.clear()


    def _create_buttons_grid(self, items):
        """Build the grid of item buttons."""
        self.items = list(items)  # current visible items
        self._clear_buttons()

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="both", expand=True, padx=5, pady=(0, UISettings.SPACING["medium"]))

        row, col = 0, 0
        for item in self.items:
            photo = self._load_image(getattr(item, "icon", None))
            text = f"{item.name}\n{item.price:.2f} €"

            btn = HoverButton(
                parent=self.buttons_frame,
                text=text,
                image=photo,
                compound="top",
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
            )
            btn.grid(
                row=row, column=col,
                padx=UISettings.SPACING["small"],
                pady=UISettings.SPACING["small"],
                sticky="nsew"
            )

            self.buttons[item.id] = btn
            btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b))
            btn.bind("<Leave>", lambda e, b=btn, i=item: self._on_leave(b, i))
            btn.configure(command=lambda i=item: self._on_select(i))

            col += 1
            if col >= BUTTON_GRID_COLS:
                col = 0
                row += 1

        # Make columns expand evenly
        for c in range(BUTTON_GRID_COLS):
            self.buttons_frame.columnconfigure(c, weight=1)

    # -------------------------------
    # Helpers
    # -------------------------------

    def _load_image(self, icon_filename):

        image_path = os.path.join(APP_SETTINGS.get("images_directory"), "products", icon_filename)
        if not os.path.exists(image_path):
            return None

        """Safely load and resize the item image."""
        if not icon_filename:
            return None
        

        image = utils.load_image(image_path)
        
        image_width = BUTTON_WIDTH * IMAGE_SCALE_FACTOR
        image_height = BUTTON_HEIGHT * IMAGE_SCALE_FACTOR
        photo = ctk.CTkImage(image, size=(image_width, image_height))
        return photo

    # -------------------------------
    # Interactivity
    # -------------------------------

    def _on_hover(self, button):
        button.configure(fg_color=UISettings.COLORS.get("hover", "#444"))

    def _on_leave(self, button, item):
        if self.selected_item and item.id == self.selected_item.id:
            button.configure(fg_color=UISettings.COLORS["secondary"])
        else:
            button.configure(fg_color=button.default_fg)

    def _on_select(self, item):
        """Handle item selection and notify callback."""
        if self.selected_item:
            prev_btn = self.buttons[self.selected_item.id]
            prev_btn.configure(fg_color=prev_btn.default_fg)

        self.selected_item = item
        btn = self.buttons[item.id]
        btn.configure(fg_color=UISettings.COLORS["secondary"])

        if self.select_callback:
            self.select_callback(item)

    # -------------------------------
    # Filtering
    # -------------------------------

    def filter_by_category(self, category):
        """
        Filter items by a category.
        If category is None, show all items.
        """
        logger.debug(f"Filtering items by category: {getattr(category, 'slug', 'All')}")

        if category is None:
            filtered_items = self._all_items
        else:
            filtered_items = [
                item for item in self._all_items
                if getattr(item, "category_id", None) == getattr(category, "id", None)
            ]

        self.selected_item = None
        self._create_buttons_grid(filtered_items)

    