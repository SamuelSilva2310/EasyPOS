import customtkinter as ctk
from easypos.ui.styles import UISettings
from easypos.ui.layout_left import LayoutLeft
from easypos.ui.layout_right import LayoutRight

from easypos.controllers.item import ItemController
from easypos.controllers.sale import SaleController
from easypos.database.seeder import import_data
import logging

from easypos.settings import APP_SETTINGS

logger = logging.getLogger(__name__)

# Set global theme for CTk
UISettings.apply_theme()


class UIApp(ctk.CTk):
    def __init__(self, sale_controller):
        super().__init__()
        self.title("EasyPOS")
        self.geometry(UISettings.APP_WINDOW_SIZE)

        self.sale_controller = sale_controller

        # Set up grid structure
        self.grid_rowconfigure(0, weight=0)  # Top bar (fixed height)
        self.grid_rowconfigure(1, weight=0)  # Separator
        self.grid_rowconfigure(2, weight=1)  # Main content (expandable)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        # Create UI components
        self.create_top_bar()
        self._configure_layout()

    def create_top_bar(self):
        # --- Top bar frame ---
        top_bar = ctk.CTkFrame(self, height=40, fg_color="#2C3E50", corner_radius=0)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        # --- Inner frame for padding ---
        inner_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        inner_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=UISettings.SPACING["medium"], pady=8)
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=0)

        # --- Left: dropdown menu ---
        menu = ctk.CTkOptionMenu(inner_frame, values=["Opções", "Importar dados", "Trocar conexão impressora"], command=self._option_menu_callback)
        menu.grid(row=0, column=0, sticky="w")



        # --- Right: settings button ---
        # --- Right: printer connection status ---
        self.lbl_printer_status = ctk.CTkLabel(
            inner_frame,
            text="🔴 Desconectado",
            text_color="red",
            font=("Arial", 14, "bold")
        )
        self.lbl_printer_status.grid(row=0, column=1, sticky="e")

        # --- Separator line ---
        separator = ctk.CTkFrame(self, height=2, fg_color="#34495E")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew")

    def _configure_layout(self):
        # --- Left frame ---
        self.leftFrame = LayoutLeft(self, self._on_item_selected)
        self.leftFrame.grid(row=2, column=0, sticky="nsew")

        # --- Right frame ---
        self.rightFrame = LayoutRight(parent=self, sale_controller=self.sale_controller)
        self.rightFrame.grid(row=2, column=1, sticky="nsew")

    def _on_item_selected(self, item):
        self.rightFrame.item_selected(item)
        ctk.filedialog.askopenfilename
        print(f"Item selected: {item.name}")

    def _option_menu_callback(self, option):
        print(f"Option menu clicked {option}")
        if option == "Importar dados":
            filepath = ctk.filedialog.askopenfilename()
            try:
                import_data(filepath)
                self._refresh_all()
            except Exception as e:
                print(f"Error importing data: {e}")
            logger.info(f"Data imported from {filepath}")
        elif option == "Trocar conexão impressora":
            from easypos.ui.windows.window_printer_config import PrinterConfigWindow
            window = PrinterConfigWindow(self)
            window.center_window()

    def _refresh_all(self):
        self.leftFrame.refresh_all()
        self.rightFrame.refresh()

    def update_printer_status(self, connected: bool, connection_type: str = None):
        """Update the printer connection status label."""
        if connected:
            label_text = f"🟢 Conectado ({connection_type or 'desconhecido'})"
            color = "#2ECC71"  # green
        else:
            label_text = f"🔴 Desconectado ({connection_type or 'desconhecido'})"
            color = "#E74C3C"  # red

        self.lbl_printer_status.configure(text=label_text, text_color=color)


    def start_status_monitor(self):
        if getattr(self, "_status_monitor_running", False):
            return
        self._status_monitor_running = True
        self._check_printer_status_loop()

    def _check_printer_status_loop(self):
        from easypos.printer.printer_manager import PrinterManager
        manager = PrinterManager.get_instance()
        printer_status = manager.status()
        self.update_printer_status(printer_status.get("connected"), printer_status.get("connection_type"))
        self.after(5000, self._check_printer_status_loop)

    def on_close(self):
        """Called when the window is closed."""
        logger.info("App is closing... saving data, cleaning up...")
        APP_SETTINGS.save()
        
        
        self.destroy()  # actually close the window

    def run(self):
        self.start_status_monitor()
        self.mainloop()
        APP_SETTINGS.save()


