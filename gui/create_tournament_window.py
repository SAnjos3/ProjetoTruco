import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import string

# Função para gerar um código de torneio aleatório e único
def generate_tournament_code(db):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        db.cursor.execute("SELECT 1 FROM tournaments WHERE code = ?", (code,))
        if not db.cursor.fetchone():
            return code

class CreateTournamentWindow:
    def __init__(self, root, db, on_tournament_created, user, on_back):
        self.root = root
        self.db = db
        self.on_tournament_created = on_tournament_created
        self.user = user  # Adiciona o usuário logado
        self.on_back = on_back  # Callback para voltar
        self.root.title("Criar Novo Torneio")
        
        # Ajuste da geometria da janela
        root.geometry("375x667")
        root.resizable(False, False)

        # Estilização da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#121212")  # Preto mais claro

        # Criação de um frame principal para organizar o layout
        main_frame = ctk.CTkFrame(root, fg_color="#121212", corner_radius=0)  # Fundo preto mais claro e sem margem
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Label e entrada para nome do torneio
        self.name_label = ctk.CTkLabel(main_frame, text="Nome do Torneio:", font=("Helvetica", 14), text_color="white")
        self.name_label.pack(pady=5)

        self.name_entry = ctk.CTkEntry(main_frame, fg_color="black", text_color="white", border_width=2, border_color="brown", corner_radius=15)
        self.name_entry.pack(pady=5)

        # Botão para criar o torneio
        self.create_button = ctk.CTkButton(main_frame, text="Criar Torneio", command=self.create_tournament, 
                                           fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=200, height=40)
        self.create_button.pack(pady=20)

        # Botão para voltar
        self.back_button = ctk.CTkButton(main_frame, text="Voltar", command=self.go_back, 
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=200, height=40)
        self.back_button.pack(pady=10)

    def create_tournament(self):
        # Captura o nome do torneio
        name = self.name_entry.get()

        if not name:
            messagebox.showerror("Erro", "Por favor, insira o nome do torneio.")
            return

        # Gera um código único para o torneio
        code = generate_tournament_code(self.db)

        # Pega o ID do usuário logado
        user_id = self.user[0] if isinstance(self.user, tuple) else self.user.user_id

        # Insere o novo torneio no banco de dados
        self.db.cursor.execute(
            "INSERT INTO tournaments (name, code, creator_user_id) VALUES (?, ?, ?)",
            (name, code, user_id)
        )
        self.db.conn.commit()

        # Adiciona o criador como jogador do torneio
        tournament_id = self.db.cursor.lastrowid

        player = self.db.cursor.execute(
            "SELECT player_id FROM players WHERE user_id = ?", (user_id,)
        ).fetchone()

        if not player:
            self.db.cursor.execute(
                "INSERT INTO players (user_id, score) VALUES (?, 0)", (user_id,)
            )
            player_id = self.db.cursor.lastrowid
        else:
            player_id = player[0]

        self.db.cursor.execute(
            "INSERT INTO match_players (tournament_id, player_id, score) VALUES (?, ?, 0)",
            (tournament_id, player_id)
        )
        self.db.conn.commit()

        # Exibe uma mensagem de sucesso e finaliza a criação
        messagebox.showinfo("Sucesso", f"Torneio criado com sucesso! Código do torneio: {code}")
        
        # Chama o callback para atualizar a lista de torneios
        self.on_tournament_created()

        # Volta para a janela de visualização de torneios
        self.go_back()

    def go_back(self):
        # Primeiro chama o callback de navegação
        self.on_back()

        # Agora destrói a janela
        self.root.destroy()
