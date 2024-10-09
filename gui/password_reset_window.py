import customtkinter as ctk
from tkinter import messagebox, simpledialog
import hashlib

class PasswordResetWindow:
    def __init__(self, root, db, on_return_to_login):  # Corrigido: __init__ com dois sublinhados
        self.root = root
        self.db = db
        self.on_return_to_login = on_return_to_login  # Callback para voltar ao login
        self.root.title("Redefinir Senha")
        
        # Ajuste do tamanho da janela
        root.geometry("375x667")
        root.resizable(False, False)

        # Estilização da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#1c1c1c")  # Define o fundo para um preto mais claro (cinza escuro)

        # Frame principal com a cor de fundo ajustada
        main_frame = ctk.CTkFrame(root, fg_color="#1c1c1c", corner_radius=10)  # Preto mais claro
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Campo para inserir o e-mail
        self.email_label = ctk.CTkLabel(main_frame, text="Digite seu e-mail:", text_color="white", font=("Helvetica", 14))
        self.email_label.pack(pady=15)
        
        self.email_entry = ctk.CTkEntry(main_frame, placeholder_text="Digite seu e-mail", fg_color="gray25", text_color="white",
                                        placeholder_text_color="gray", font=("Helvetica", 14), corner_radius=10)
        self.email_entry.pack(pady=10, fill="x")

        # Botão para redefinir a senha
        self.reset_button = ctk.CTkButton(main_frame, text="Redefinir Senha", command=self.reset_password,
                                          fg_color="black", text_color="white", hover_color="gray30",
                                          corner_radius=15, border_width=2, border_color="brown",  # Borda marrom
                                          width=200, height=40)
        self.reset_button.pack(pady=20)

        # Botão para voltar ao login
        self.back_button = ctk.CTkButton(main_frame, text="Voltar ao Login", command=self.go_back,
                                         fg_color="black", text_color="white", hover_color="gray30",
                                         corner_radius=15, border_width=2, border_color="brown",  # Borda marrom
                                         width=200, height=40)
        self.back_button.pack(pady=10)

    def reset_password(self):
        email = self.email_entry.get()

        # Verifica se o e-mail existe no banco de dados
        user = self.db.cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user:
            # Pede a nova senha
            new_password = simpledialog.askstring("Nova Senha", "Digite a nova senha:", show="*")
            
            if new_password:
                # Atualiza a senha no banco de dados
                password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                self.db.cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (password_hash, email))
                self.db.conn.commit()
                messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
                self.on_return_to_login()  # Volta para a tela de login após o sucesso
                self.root.destroy()  # Fecha a janela de redefinição de senha
        else:
            messagebox.showerror("Erro", "E-mail não encontrado.")

    def go_back(self):
        self.root.destroy()
        self.on_return_to_login()
