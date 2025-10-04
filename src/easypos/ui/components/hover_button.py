import customtkinter as ctk

class HoverButton(ctk.CTkButton):
    def __init__(self, parent=None, hover_fg="#2E7D32", **kwargs):
        """
        A CTkButton that changes color on hover, then restores theme default.
        """
        super().__init__(parent, **kwargs)

        self.default_fg = self.cget("fg_color")  # store default (theme color)
        self.hover_fg = hover_fg

        # # Bind hover events
        # self.bind("<Enter>", self._on_hover)
        # self.bind("<Leave>", self._on_leave)

    # def _on_hover(self, event):
    #     self.configure(fg_color=self.hover_fg)

    # def _on_leave(self, event):
    #     self.configure(fg_color=self.default_fg)