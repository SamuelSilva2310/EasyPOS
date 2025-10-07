import customtkinter as ctk

class UISettings:

    # --- Paths ---
    IMAGES_PATH = "images"

    # --- Global UI theme settings ---
    THEME_MODE = "System"            # options: "light", "dark", "system"
    COLOR_THEME = "blue"           # options: "blue", "green", "dark-blue"
    FONT_FAMILY = "Arial"
    FONT_SIZE_TITLE = 18
    FONT_SIZE_TEXT = 18
    APP_WINDOW_SIZE = "1000x800"

    # --- Color palette ---
    COLORS = {
        "primary": "#1E88E5",      # main accent color (e.g. buttons)
        "secondary": "#3949AB",    # secondary accent (e.g. highlights)
        "background": "#202124",   # main background
        "surface": "#2E2E2E",      # frames, cards
        "text": "#FFFFFF",         # primary text
        "text_muted": "#B0B0B0",   # muted text
        "success": "#43A047",      # green success
        "warning": "#FB8C00",      # orange warning
        "error": "#E53935",        # red error
        "hover": "#3A3A3A",        # generic hover color
    }

    # --- Padding and spacing ---
    SPACING = {
        "small": 5,
        "medium": 10,
        "large": 20
    }

    @classmethod
    def apply_theme(cls):
        """Applies the global CustomTkinter theme and appearance."""
        ctk.set_appearance_mode(cls.THEME_MODE)
        ctk.set_default_color_theme(cls.COLOR_THEME)

    @classmethod
    def style_button(cls, button: ctk.CTkButton, variant="primary"):
        """Apply consistent button style based on variant."""
        color = cls.COLORS.get(variant, cls.COLORS["primary"])
        button.configure(
            fg_color=color,
            hover_color=cls._darker(color, 0.85),
            text_color=cls.COLORS["text"]
        )
    
    @classmethod
    def style_title(cls, title: ctk.CTkLabel, primary=False):
        """Apply consistent title style."""
        #color = cls.COLORS["primary"] if primary else cls.COLORS["secondary"]
        title.configure(font=(cls.FONT_FAMILY, cls.FONT_SIZE_TITLE, "bold"))

    @staticmethod
    def _darker(hex_color, factor=0.9):
        """Return a slightly darker version of a hex color."""
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(max(int(c * factor), 0) for c in rgb)
        return f"#{''.join(f'{v:02X}' for v in dark_rgb)}"