import customtkinter as ctk
from PIL import Image, ImageTk
import os
import logging
from easypos.ui.settings import UISettings

logger = logging.getLogger(__name__)

class ActionsFrame(ctk.CTkFrame):
    def __init__(self, parent, sale_controller, button_width=120, button_height=80):
        super().__init__(parent)
        self.sale_controller = sale_controller

        self.item = None
        self.button_width = button_width
        self.button_height = button_height

        # State variables
        self.quantity_var = ctk.StringVar(value="1")
        self.money_var = ctk.StringVar(value="")

        # Layout
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=0)
        self.grid_columnconfigure((0, 1), weight=1)

        self._create_components()

    def _create_components(self):
        padding_y = 6
        padding_x = 8

        # --- Item Header ---
        self.icon_label = ctk.CTkLabel(self, text="", width=60, height=60)
        self.icon_label.grid(row=0, column=0, columnspan=2, pady=(10, 4))

        self.title_label = ctk.CTkLabel(
            self,
            text="Selecione um artigo",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # --- Item info section ---
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=padding_x)

        # Quantity
        ctk.CTkLabel(info_frame, text="Quantidade:").grid(row=0, column=0, sticky="e", padx=padding_x, pady=padding_y)
        self.input_quantity = ctk.CTkEntry(info_frame, textvariable=self.quantity_var, width=80)
        self.input_quantity.grid(row=0, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # Unit Price
        ctk.CTkLabel(info_frame, text="Preço unitário:").grid(row=1, column=0, sticky="e", padx=padding_x, pady=padding_y)
        self.label_item_price = ctk.CTkLabel(info_frame, text="0,00 €")
        self.label_item_price.grid(row=1, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # Total
        ctk.CTkLabel(info_frame, text="Total:").grid(row=2, column=0, sticky="e", padx=padding_x, pady=padding_y)
        self.label_total_price = ctk.CTkLabel(info_frame, text="0,00 €", font=ctk.CTkFont(weight="bold"))
        self.label_total_price.grid(row=2, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # --- Payment section ---
        payment_frame = ctk.CTkFrame(self, fg_color="transparent")
        payment_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=padding_x, pady=(10, 0))

        ctk.CTkLabel(payment_frame, text="Dinheiro recebido:").grid(row=0, column=0, sticky="e", padx=padding_x, pady=padding_y)
        self.input_money_handed = ctk.CTkEntry(payment_frame, textvariable=self.money_var, width=100)
        self.input_money_handed.grid(row=0, column=1, sticky="w", padx=padding_x, pady=padding_y)

        ctk.CTkLabel(payment_frame, text="Troco:").grid(row=1, column=0, sticky="e", padx=padding_x, pady=padding_y)
        self.label_change = ctk.CTkLabel(payment_frame, text="0,00 €", font=ctk.CTkFont(weight="bold"))
        self.label_change.grid(row=1, column=1, sticky="w", padx=padding_x, pady=padding_y)

        # --- Sell button ---
        self.button_sell = ctk.CTkButton(
            self,
            text="💰 Vender",
            command=self.sell,
            height=38,
            width=150,
            corner_radius=10,
        )
        self.button_sell.grid(row=4, column=0, columnspan=2, pady=(15, 10))

        # Binds
        self.quantity_var.trace_add("write", self._on_change)
        self.money_var.trace_add("write", self._on_change)

    def update_ui(self, item):

        self.item = item
        self.title_label.configure(text=item.name)

        self.quantity_var.set("1")
        self.money_var.set("")
        self.label_item_price.configure(text=f"{item.price:.2f} €")
        self.label_total_price.configure(text=f"{item.price:.2f} €")
        self.label_change.configure(text="0,00 €")

        image_path = os.path.join("images", getattr(item, "icon", ""))
        if hasattr(item, "icon") and item.icon and os.path.exists(image_path):
            img = Image.open(image_path).resize((60, 60))
            photo = ImageTk.PhotoImage(img)
            self.icon_label.configure(image=photo, text="")
            self.icon_label.image = photo
        else:
            self.icon_label.configure(image="", text="")

    def _on_change(self, *args):
        """Recalcula o total e o troco quando a quantidade ou o dinheiro mudam."""
        if not self.item:
            return

        try:
            quantity = int(self.quantity_var.get())
            if quantity < 0:
                quantity = 0
        except ValueError:
            quantity = 0

        total = self.item.price * quantity
        self.label_total_price.configure(text=f"{total:.2f} €")

        try:
            money = float(self.money_var.get())
        except ValueError:
            money = 0.0

        change = money - total
        self.label_change.configure(text=f"{change:.2f} €")

    def sell(self):
        """Executa a venda do item selecionado."""
        if not self.item:
            ctk.CTkMessagebox.show_warning("Nenhum item", "Selecione um artigo primeiro.")
            return

        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            ctk.CTkMessagebox.show_error("Quantidade inválida", "Insira uma quantidade válida.")
            return

        logger.info(f"Vendendo {quantity} de {self.item.name}")
        self.sale_controller.make_sale(self.item.id, quantity)