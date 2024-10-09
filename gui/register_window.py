import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import hashlib
from logic.database import Database

class RegisterWindow:
    def __init__(self, root, on_return_to_login):
        self.root = root
        self.db = Database()  # Inicializa o banco de dados
        self.on_return_to_login = on_return_to_login  # Callback para voltar ao login
        self.root.title("Cadastro - Truco Ranker")
        
        # Ajuste da geometria e configurações de aparência
        root.geometry("375x667")
        root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="black")

        # Frame principal para o layout
        main_frame = ctk.CTkFrame(root, fg_color="black", corner_radius=10)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Elementos da janela de cadastro (Caixas de entrada com o mesmo estilo do login)
        self.username_label = ctk.CTkLabel(main_frame, text="Usuário:", font=("Helvetica", 14), text_color="white")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(main_frame, placeholder_text="Digite seu usuário", width=300, height=40, corner_radius=15)
        self.username_entry.pack(pady=10)

        self.email_label = ctk.CTkLabel(main_frame, text="Email:", font=("Helvetica", 14), text_color="white")
        self.email_label.pack(pady=10)
        self.email_entry = ctk.CTkEntry(main_frame, placeholder_text="Digite seu email", width=300, height=40, corner_radius=15)
        self.email_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(main_frame, text="Senha:", font=("Helvetica", 14), text_color="white")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(main_frame, placeholder_text="Digite sua senha", show="*", width=300, height=40, corner_radius=15)
        self.password_entry.pack(pady=10)

        # Botão para cadastrar (Tamanho e estilo igual ao login)
        self.register_button = ctk.CTkButton(main_frame, text="Cadastrar", command=self.register, 
                                             fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown",
                                             width=300, height=40)
        self.register_button.pack(pady=20)

        # Botão para voltar à tela de login (Tamanho e estilo igual ao login)
        self.back_button = ctk.CTkButton(main_frame, text="Voltar para Login", command=self.return_to_login,
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown",
                                         width=300, height=40)
        self.back_button.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Verificar se todos os campos estão preenchidos
        if not username or not email or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Verificar se o nome de usuário já existe no banco de dados
        existing_user = self.db.cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            messagebox.showerror("Erro", "Nome de usuário já existe. Escolha outro.")
            return
        
        # Verificar se o email já existe no banco de dados
        existing_email = self.db.cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if existing_email:
            messagebox.showerror("Erro", "Email já cadastrado. Use outro email.")
            return

        # Criação do hash da senha
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Inserir o novo usuário no banco de dados
        self.db.cursor.execute(
            "INSERT INTO users (username, email, password_hash, name) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, username)  # Usando o nome como "name" também
        )
        self.db.conn.commit()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        
        # Fechar a janela de cadastro e chamar a função para abrir a janela de login
        self.root.destroy()
        self.on_return_to_login()  # Chama o callback para abrir a tela de login

    def return_to_login(self):
        self.root.destroy()
        self.on_return_to_login()
