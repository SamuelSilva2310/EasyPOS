class TicketStyles:
    # --- Image scaling ---
    LOGO_SCALE_FACTOR = 0.6      # Slightly smaller
    ICON_IMAGE_WIDTH = 180
    ICON_IMAGE_SCALE_FACTOR = 1.0

    # --- Text styles ---
    STYLE_HEADER_TITLE = {
        "align": "center",
        "bold": True,
        "custom_size": True,
        "width": 2,
        "height": 2
    }

    STYLE_HEADER_SUBTITLE = {
        "align": "center",
        "bold": False,
        "custom_size": True,
        "width": 1,
        "height": 1
    }


    STYLE_BODY = {
        "align": "left",
        "bold": False,
        "custom_size": False
    }


    STYLE_INFO = {
        "align": "center",
        "bold": False,
        "custom_size": True,
        "width": 1,
        "height": 2
    }

    # --- Spacing ---
    SPACER_SMALL = "\n"
    SPACER_MEDIUM = "\n\n"