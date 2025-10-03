import customtkinter as ctk
import os
from PIL import Image, ImageTk

BUTTON_GRID_COLS = 3

class ItemsFrame(ctk.CTkFrame):
    def __init__(self, parent, items, select_callback=None, button_width=120, button_height=80):
        """
        :param parent: Parent tk.Frame or tk.Tk
        :param items: list of objects with .id, .name, optional .icon (path)
        :param select_callback: function called when item is selected
        """
        super().__init__(parent)
        self.items = items
        self.select_callback = select_callback
        self.selected_item = None
        self.buttons = {}        # store buttons keyed by item.id
        self.button_images = {}  # store PhotoImage references to avoid garbage collection
        self.button_width = button_width
        self.button_height = button_height

        self._create_buttons()

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
                    img = img.resize((int(self.button_width * 0.7), int(self.button_height * 0.7)))
                    photo = ImageTk.PhotoImage(img)
                    self.button_images[item.id] = photo  # keep reference

            # Create CTkButton
            btn = ctk.CTkButton(
                self,
                text=item.name,
                image=photo,
                compound="top",  # image above text
                width=self.button_width,
                height=self.button_height,
                #wraplength=100,
                fg_color="lightgray",
                hover_color="gray"
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

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
        if self.selected_item is None or button != self.buttons[self.selected_item.id]:
            button.configure(fg_color="darkgray")

    def _on_leave(self, button, item):
        if self.selected_item and item.id == self.selected_item.id:
            button.configure(fg_color="lightblue")
        else:
            button.configure(fg_color="lightgray")

    def _on_select(self, item):
        # Deselect previous
        if self.selected_item:
            prev_btn = self.buttons[self.selected_item.id]
            prev_btn.configure(fg_color="lightgray")

        # Select new
        self.selected_item = item
        btn = self.buttons[item.id]
        btn.configure(fg_color="lightblue")

        # Call external callback
        if self.select_callback:
            self.select_callback(item)