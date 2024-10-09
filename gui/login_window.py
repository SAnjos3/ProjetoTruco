import customtkinter as ctk
from tkinter import messagebox
from logic.database import Database
from PIL import Image  # Certifique-se de ter a biblioteca PIL instalada
import os  # Para verificar o caminho do arquivo

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Login - Truco Ranker")
        self.db = Database()  # Instância do banco de dados
        self.on_success = on_success

        # Configurando a aparência e o tamanho da janela
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        root.geometry("375x667")
        root.configure(bg="black")

        # Elementos da janela de login
        self.username_label = ctk.CTkLabel(root, text="Usuário:", font=("Helvetica", 14, "bold"), text_color="white")
        self.username_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(root, font=("Helvetica", 12), corner_radius=10,
                                           fg_color="black", text_color="white", border_width=2, border_color="brown")
        self.username_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(root, text="Senha:", font=("Helvetica", 14, "bold"), text_color="white")
        self.password_label.pack(pady=10)

        self.password_entry = ctk.CTkEntry(root, show="*", font=("Helvetica", 12), corner_radius=10,
                                           fg_color="black", text_color="white", border_width=2, border_color="brown")
        self.password_entry.pack(pady=10)

        # Botão para realizar o login
        self.login_button = ctk.CTkButton(root, text="Login", command=self.login, corner_radius=15,
                                          fg_color="black", text_color="white", hover_color="brown", border_width=2, border_color="brown")
        self.login_button.pack(pady=20)

        # Botão para abrir a janela de cadastro
        self.register_button = ctk.CTkButton(root, text="Cadastrar", command=self.open_register_window, corner_radius=15,
                                             fg_color="black", text_color="white", hover_color="brown", border_width=2, border_color="brown")
        self.register_button.pack(pady=10)

        # Botão para abrir a janela de redefinição de senha
        self.reset_button = ctk.CTkButton(root, text="Esqueci minha senha", command=self.open_password_reset_window, corner_radius=15,
                                          fg_color="black", text_color="white", hover_color="brown", border_width=2, border_color="brown")
        self.reset_button.pack(pady=10)

        # Chamar a função para carregar a imagem
        self.load_image()  # Carregar a imagem logo após os elementos de interface

    def load_image(self):
        """Função para carregar ou recarregar a imagem"""
        try:
            # Definir o caminho absoluto para a imagem
            image_path = os.path.join(os.getcwd(), "assets", "truco.png")

            # Verificar se o arquivo existe
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

            pil_image = Image.open(image_path)
            self.image_ctk = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(100, 100))

            # Cria o rótulo de imagem e o armazena permanentemente
            self.image_label = ctk.CTkLabel(self.root, image=self.image_ctk, text="")  # Sem texto
            self.image_label.pack(pady=20)

            # Manter uma referência da imagem para evitar que o Python a descarte
            self.root.image_reference = self.image_ctk
            print("Imagem carregada com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Autenticar o usuário no banco de dados
        user = self.db.authenticate_user(username, password)

        if user:
            self.on_success(user)  # Callback de sucesso
            self.root.destroy()  # Destroi a janela de login após login bem-sucedido
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def open_register_window(self):
        register_root = ctk.CTkToplevel()  # Nova janela de cadastro
        from gui.register_window import RegisterWindow  # Evita importação circular
        RegisterWindow(register_root, self.root)  # Passa a janela principal para voltar depois
        register_root.grab_set()  # Foco na nova janela

    def open_password_reset_window(self):
        reset_root = ctk.CTkToplevel()  # Nova janela de redefinição de senha
        from gui.password_reset_window import PasswordResetWindow  # Evita importação circular
        PasswordResetWindow(reset_root, self.db, self.root)  # Passa a janela principal para voltar depois
        reset_root.grab_set()  # Foco na nova janela

