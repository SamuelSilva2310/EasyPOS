import customtkinter as ctk
import logging

logger = logging.getLogger(__name__)

class AppInfoWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre o App")
        self.geometry("800x600")
        self.resizable(False, False)

        # --- Layout ---
        self._create_title()
        self._create_author()
        self._create_legal_text()
        self._create_close_button()
        self.center_window()

    def _create_title(self):
        ctk.CTkLabel(
            self,
            text="EasyPOS",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

    def _create_author(self):
        ctk.CTkLabel(
            self,
            text="Autor: Samuel Silva",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 20))

    def _create_legal_text(self):
        legal_frame = ctk.CTkFrame(self)
        legal_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        legal_text = (
            "A presente aplicação informática foi concebida, desenvolvida e detida por Samuel Silva, "
            "titular de todos os direitos de autor e demais direitos de propriedade intelectual, nos termos "
            "do Código do Direito de Autor e dos Direitos Conexos, nomeadamente, dos artigos 9.º, 11.º, 14.º "
            "e 67.º do Código do Direito de Autor e dos Direitos Conexos, aprovado pelo Decreto-Lei n.º 63/85, "
            "de 14 de março, com as suas posteriores alterações.\n\n"
            "A aplicação é cedida temporariamente, a título gratuito e para fins exclusivamente internos, "
            "à Associação de Festas Populares do Pinhal Novo.\n\n"
            "É expressamente proibida a reprodução, modificação, distribuição ou utilização para outros fins "
            "sem autorização prévia e escrita do autor.\n\n"
            "©️ 2025 Samuel Silva. Todos os direitos reservados."
        )
        ctk.CTkLabel(
            legal_frame,
            text=legal_text,
            wraplength=350,
            justify="left"
        ).pack(padx=10, pady=10)

    def _create_close_button(self):
        btn_close = ctk.CTkButton(self, text="Fechar", command=self.destroy)
        btn_close.pack(pady=(0, 15))

    def center_window(self):
        """Center this window relative to its master."""
        self.update_idletasks()

        if self.master is not None:
            master_x = self.master.winfo_x()
            master_y = self.master.winfo_y()
            master_w = self.master.winfo_width()
            master_h = self.master.winfo_height()
        else:
            master_x = master_y = 0
            master_w = self.winfo_screenwidth()
            master_h = self.winfo_screenheight()

        win_w = self.winfo_width()
        win_h = self.winfo_height()

        x = master_x + (master_w // 2 - win_w // 2)
        y = master_y + (master_h // 2 - win_h // 2)

        self.geometry(f"+{x}+{y}")