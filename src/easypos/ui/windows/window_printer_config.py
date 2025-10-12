import customtkinter as ctk
from easypos.printer.printer_manager import PrinterManager
import logging
from easypos.settings import APP_SETTINGS
import re

logger = logging.getLogger(__name__)



class PrinterConfigWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Configurar Impressora")
        self.geometry("400x380")
        self.resizable(False, False)
        self.manager = PrinterManager.get_instance()

        self.message_label = None

        # --- Layout ---
        self._create_tabs()
        self._create_message_area()
        self._create_action_buttons()

    def _create_tabs(self):
        """Creates tabs for connection types"""
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        # --- USB Tab ---
        tab_usb = self.tabs.add("USB")
        printer_connection_args = APP_SETTINGS.get("printer_connection_args", {}).get("usb", {})

        ctk.CTkLabel(tab_usb, text="Vendor ID:").pack(anchor="w", padx=10, pady=(10, 0))
        self.usb_vendor_id = ctk.CTkEntry(tab_usb, placeholder_text="e.g. 0x10c4")
        self.usb_vendor_id.pack(fill="x", padx=10)
        if "idVendor" in printer_connection_args:
            self.usb_vendor_id.insert(0, str(printer_connection_args["idVendor"]))

        ctk.CTkLabel(tab_usb, text="Product ID:").pack(anchor="w", padx=10, pady=(10, 0))
        self.usb_product_id = ctk.CTkEntry(tab_usb, placeholder_text="e.g. 0xea60")
        self.usb_product_id.pack(fill="x", padx=10)
        if "idProduct" in printer_connection_args:
            self.usb_product_id.insert(0, str(printer_connection_args["idProduct"]))

        # --- Network Tab ---
        tab_network = self.tabs.add("Network")
        printer_connection_args = APP_SETTINGS.get("printer_connection_args", {}).get("network", {})

        ctk.CTkLabel(tab_network, text="Endereço IP:").pack(anchor="w", padx=10, pady=(10, 0))
        self.net_ip = ctk.CTkEntry(tab_network, placeholder_text="e.g. 192.168.0.100")
        self.net_ip.pack(fill="x", padx=10)
        if "host" in printer_connection_args:
            self.net_ip.insert(0, printer_connection_args["host"])

        ctk.CTkLabel(tab_network, text="Porta:").pack(anchor="w", padx=10, pady=(10, 0))
        self.net_port = ctk.CTkEntry(tab_network, placeholder_text="9100")
        self.net_port.pack(fill="x", padx=10)
        if "port" in printer_connection_args:
            self.net_port.insert(0, str(printer_connection_args["port"]))

        # --- Fake Tab ---
        tab_fake = self.tabs.add("Fake")
        printer_connection_args = APP_SETTINGS.get("printer_connection_args", {}).get("fake", {})
        ctk.CTkLabel(tab_fake, text="Isto e falso:").pack(anchor="w", padx=10, pady=(10, 0))
        
    def center_window(self):
        """Center this window relative to its master."""
        self.update_idletasks()  # Ensure geometry info is updated

        # Get master (parent) geometry
        if self.master is not None:
            master_x = self.master.winfo_x()
            master_y = self.master.winfo_y()
            master_w = self.master.winfo_width()
            master_h = self.master.winfo_height()
        else:
            master_x = master_y = 0
            master_w = self.winfo_screenwidth()
            master_h = self.winfo_screenheight()

        # Get this window's width/height
        win_w = self.winfo_width()
        win_h = self.winfo_height()

        # Compute centered coordinates
        x = master_x + (master_w // 2 - win_w // 2)
        y = master_y + (master_h // 2 - win_h // 2)

        # Apply position
        self.geometry(f"+{x}+{y}")
    def _create_message_area(self):
        """Fixed area for feedback messages"""
        self.message_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.message_frame.pack(fill="x", pady=(0, 5))
        self.message_label = ctk.CTkLabel(self.message_frame, text="", text_color="white")
        self.message_label.pack()

    def _create_action_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(10, 15))

        btn_connect = ctk.CTkButton(frame, text="Conectar", command=self._on_connect)
        btn_connect.pack(side="right", padx=(0, 15))

        btn_cancel = ctk.CTkButton(frame, text="Cancelar", fg_color="gray", command=self.destroy)
        btn_cancel.pack(side="right", padx=10)

    def show_message(self, message, color="white"):
        """Show message in the fixed label"""
        self.message_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.message_label.configure(text=""))

    def _on_connect(self):
        """Connect printer based on selected tab"""
        selected_tab = self.tabs.get()
        logger.info(f"Connecting printer via {selected_tab}")

        try:
            if selected_tab == "USB":
                vendor_str = self.usb_vendor_id.get().strip()
                product_str = self.usb_product_id.get().strip()

                if not vendor_str or not product_str:
                    return self.show_message("Preencha Vendor ID e Product ID", "orange")

                # Handle hex or decimal
                try:
                    id_vendor = int(vendor_str, 16 if vendor_str.startswith("0x") else 10)
                    id_product = int(product_str, 16 if product_str.startswith("0x") else 10)
                except ValueError:
                    return self.show_message("IDs devem ser números válidos", "red")

                args = {"idVendor": id_vendor, "idProduct": id_product}
                conn_type = "usb"

            elif selected_tab == "Network":
                ip = self.net_ip.get().strip()
                port_str = self.net_port.get().strip()

                if not ip or not port_str:
                    return self.show_message("⚠️ Preencha IP e porta", "orange")

                if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
                    return self.show_message("IP inválido", "red")

                try:
                    port = int(port_str)
                except ValueError:
                    return self.show_message("Porta inválida", "red")

                args = {"host": ip, "port": port}
                conn_type = "network"

            elif selected_tab == "Fake":
                args = {}
                conn_type = "fake"
            else:
                return self.show_message("Tipo de conexão inválido", "red")

            # Attempt connection
            connected = self.manager.connect(conn_type, args)
            logger.info(self.manager.status())
            if connected:
                self.show_message("Impressora conectada com sucesso!", "green")
                self.after(1500, self.destroy)
            else:
                self.show_message("Erro ao conectar à impressora", "red")

            APP_SETTINGS.set("printer_connection_type", conn_type)
            APP_SETTINGS.set("printer_connection_args", args)

        except Exception as e:
            logger.error(f"Erro ao conectar impressora: {e}")
            self.show_message(f"Erro: {e}", "red")