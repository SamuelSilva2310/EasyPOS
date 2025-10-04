import customtkinter as ctk
import os
from PIL import Image, ImageTk
from easypos.ui.settings import UISettings
from easypos.ui.components.hover_button import HoverButton

BUTTON_GRID_COLS = 3
IMAGE_SCALE_FACTOR = 0.6
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 120

class ItemsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, items, select_callback=None):
        """
        :param parent: Parent tk.Frame or tk.Tk
        :param items: list of objects with .id, .name, optional .icon (path)
        :param select_callback: function called when item is selected
        """
        super().__init__(parent)
        self._style()
        self.items = items
        self.select_callback = select_callback
        self.selected_item = None
        self.buttons = {}        # store buttons keyed by item.id
        self.button_images = {}  # store PhotoImage references to avoid garbage collection


        self._create_buttons()
    
    def _style(self):
        self.configure(border_width=1, corner_radius=0)


    def _create_buttons(self):
        row = 0
        col = 0

        for item in self.items:
            # Prepare image if available
            photo = None
            if hasattr(item, "icon") and item.icon:
                img_path = os.path.join("images", item.icon)
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    image_width = BUTTON_WIDTH * IMAGE_SCALE_FACTOR
                    image_height = BUTTON_HEIGHT * IMAGE_SCALE_FACTOR
                    #img = img.resize((int(self.button_width * IMAGE_SCALE_FACTOR), int(self.button_height * IMAGE_SCALE_FACTOR)))
                    photo = ctk.CTkImage(img, size=(image_width, image_height))
                    self.button_images[item.id] = photo  # keep reference

            # Create CTkButton
            btn = HoverButton(
                parent=self,
                text=item.name,
                image=photo,
                compound="top",  # image above text
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                #hover_fg=UISettings.COLORS["hover"],
                #wraplength=100,
                #hover_color="red"
            )

            #UISettings.style_button(btn)
            btn.grid(row=row, column=col, padx=5, pady=UISettings.SPACING.get("medium"), sticky="nsew")

            # Store button
            self.buttons[item.id] = btn

            # Hover and selection bindings
            btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b))
            btn.bind("<Leave>", lambda e, b=btn, i=item: self._on_leave(b, i))
            btn.configure(command=lambda i=item: self._on_select(i))

            # Update row/column
            col += 1
            if col >= BUTTON_GRID_COLS:
                col = 0
                row += 1

        # Make columns expand evenly
        for c in range(BUTTON_GRID_COLS):
            self.grid_columnconfigure(c, weight=1)

    def _on_hover(self, button):
        pass
        

    def _on_leave(self, button, item):
        pass
        # if self.selected_item and item.id == self.selected_item.id:
        #     button.configure(fg_color=UISettings.COLORS["secondary"])
        # else:
        #     button.configure(fg_color=button.default_fg)

    def _on_select(self, item):

        #for item_id, button in self.buttons.items():
        # Deselect previous
        if self.selected_item:
            prev_btn = self.buttons[self.selected_item.id]
            prev_btn.configure(fg_color=prev_btn.default_fg)

        # Select new
        self.selected_item = item
        btn = self.buttons[item.id]
        btn.configure(fg_color=UISettings.COLORS["secondary"])

        # Call external callback
        if self.select_callback:
            self.select_callback(item)
        
