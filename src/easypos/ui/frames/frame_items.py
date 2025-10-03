import tkinter as tk
import os
from PIL import Image, ImageTk

class ItemsFrame(tk.Frame):
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
        for item in self.items:
            # Prepare image if available
            photo = None
            if hasattr(item, "icon") and item.icon:
                # photo = tk.PhotoImage(file=os.path.join("images", item.icon))
                # photo = photo.subsample(3, 3)
                img = Image.open(os.path.join("images", item.icon)) # convert to grayscale (item.icon)
                img = img.resize((int(self.button_width * 0.7), int(self.button_height * 0.7)))  # adjust as needed
                photo = ImageTk.PhotoImage(img)
                self.button_images[item.id] = photo  # keep reference
            
            #photo = None # Debug
            btn = tk.Button(
                self,
                text=item.name,
                image=photo,
                compound=tk.TOP,       # image above text
                width=self.button_width,             # in text units
                height=self.button_height,             # in text units
                wraplength=100,       # pixels for text wrapping
                relief="raised",
                bg="lightgray",
            )
            # btn = tk.Button(
            #     self,
            #     text=item.name,
            #     image=photo,
            #     compound="top",  # image above text
            #     width=self.button_width // 10,
            #     height=self.button_height // 20,
            #     relief="raised",
            #     bg="lightgray",
            #     wraplength=self.button_width - 10,
            #     justify="center"
            # )
            btn.pack(padx=5, pady=5)
            self.buttons[item.id] = btn

            # Bind hover events
            btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b))
            btn.bind("<Leave>", lambda e, b=btn, i=item: self._on_leave(b, i))

            # Selection
            btn.config(command=lambda i=item: self._on_select(i))

    def _on_hover(self, button):
        # Only hover effect if not selected
        if self.selected_item is None or button != self.buttons[self.selected_item.id]:
            button.config(bg="darkgray")

    def _on_leave(self, button, item):
        # Restore color based on selection
        if self.selected_item and item.id == self.selected_item.id:
            button.config(bg="lightblue")
        else:
            button.config(bg="lightgray")

    def _on_select(self, item):
        # Deselect previous
        if self.selected_item:
            prev_btn = self.buttons[self.selected_item.id]
            prev_btn.config(bg="lightgray", relief="raised")

        # Select new
        self.selected_item = item
        btn = self.buttons[item.id]
        btn.config(bg="lightblue", relief="sunken")

        # Call external callback
        if self.select_callback:
            self.select_callback(item)