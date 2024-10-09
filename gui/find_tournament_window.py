import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gui.tournament_details_window import TournamentDetailsWindow  # Certifique-se de que o caminho esteja correto

class FindTournamentWindow:
    def __init__(self, root, db, on_tournament_joined, user, on_back):
        self.root = root
        self.db = db
        self.on_tournament_joined = on_tournament_joined  # Callback para atualizar torneios
        self.user = user  # Adiciona o usuário logado
        self.on_back = on_back  # Callback para voltar à janela anterior
        self.root.title("Achar Torneio")
        
        # Ajuste da geometria da janela
        root.geometry("375x667")
        root.resizable(False, False)

        # Estilização da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#121212")  # Preto mais claro

        # Criação de um frame principal para organizar o layout
        main_frame = ctk.CTkFrame(root, fg_color="#121212", corner_radius=0)  # Fundo preto mais claro sem margens
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Campo para inserir o código do torneio
        self.code_label = ctk.CTkLabel(main_frame, text="Código do Torneio:", font=("Helvetica", 14), text_color="white")
        self.code_label.pack(pady=5)

        self.code_entry = ctk.CTkEntry(main_frame, fg_color="black", text_color="white", border_width=2, border_color="brown", corner_radius=15)
        self.code_entry.pack(pady=5)

        # Botão para encontrar o torneio
        self.find_button = ctk.CTkButton(main_frame, text="Entrar no Torneio", command=self.find_tournament, 
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=200, height=40)
        self.find_button.pack(pady=10)

        # Botão para voltar
        self.back_button = ctk.CTkButton(main_frame, text="Voltar", command=self.go_back, 
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=200, height=40)
        self.back_button.pack(pady=10)

    def find_tournament(self):
        code = self.code_entry.get()

        if not code:
            messagebox.showerror("Erro", "Por favor, insira o código do torneio.")
            return

        # Verifica se o código do torneio existe
        tournament = self.db.cursor.execute(
            "SELECT tournament_id FROM tournaments WHERE code = ?", (code,)
        ).fetchone()

        if tournament:
            tournament_id = tournament[0]

            # Verifica se o jogador já está inscrito no torneio
            player_id = self.get_current_player_id()

            # Se não foi possível obter o player_id, interrompe a execução
            if player_id is None:
                return

            already_in_tournament = self.db.cursor.execute(
                "SELECT 1 FROM match_players WHERE tournament_id = ? AND player_id = ?",
                (tournament_id, player_id)
            ).fetchone()

            if already_in_tournament:
                messagebox.showinfo("Aviso", "Você já está inscrito neste torneio!")
                return

            # Insere o jogador no torneio
            self.db.cursor.execute(
                "INSERT INTO match_players (tournament_id, player_id, score) VALUES (?, ?, 0)",
                (tournament_id, player_id)
            )
            self.db.conn.commit()

            messagebox.showinfo("Sucesso", f"Você entrou no torneio com sucesso!")

            # Atualiza a lista de torneios
            self.on_tournament_joined()

            # Fecha a janela de encontrar torneio
            if self.root.winfo_exists():  # Verifica se a janela ainda existe antes de destruí-la
                self.root.destroy()

            # Abre a janela de detalhes do torneio, sem usar self.root, criando uma nova janela
            tournament_details_root = ctk.CTkToplevel()  # Usando ctk.Toplevel
            tournament_details_window = TournamentDetailsWindow(tournament_details_root, self.db, tournament_id, self.on_back)
            tournament_details_root.geometry("375x667")  # Definir um tamanho adequado para a janela de detalhes
            tournament_details_root.mainloop()
        else:
            messagebox.showerror("Erro", "Código do torneio não encontrado.")

    def get_current_player_id(self):
        # Função que busca o player_id do jogador logado a partir do self.user
        user_id = self.user[0]  # ID do usuário logado
        player = self.db.cursor.execute(
            "SELECT player_id FROM players WHERE user_id = ?", (user_id,)
        ).fetchone()
    
        if player is None:
            # Se o jogador não estiver registrado na tabela 'players', insira-o automaticamente
            self.db.cursor.execute(
                "INSERT INTO players (user_id, score) VALUES (?, 0)", (user_id,)
            )
            self.db.conn.commit()
    
            # Recuperar o ID do jogador recém-criado
            player_id = self.db.cursor.lastrowid
            return player_id
    
        return player[0]

    def go_back(self):
        if self.root.winfo_exists():  # Verifica se a janela ainda existe antes de destruí-la
            self.root.destroy()
        self.on_back()
        
