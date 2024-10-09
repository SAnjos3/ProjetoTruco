import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class MatchCounterWindow:
    def __init__(self, root, db, match_id, team1, team2, on_match_end):
        self.root = root
        self.db = db
        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2
        self.on_match_end = on_match_end
        
        self.team1_score = 0
        self.team2_score = 0

        # Configuração da janela
        self.root.title("Contador de Pontos")
        self.root.geometry("375x667")  # Ajuste para tamanho de celular
        self.root.resizable(False, False)

        # Estilização da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="black")  # Define o fundo da janela como preto

        # Frame principal
        main_frame = ctk.CTkFrame(root, fg_color="black", corner_radius=10)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Labels dos times
        self.team1_label = ctk.CTkLabel(main_frame, text=f"Time 1: {', '.join(team1)}", font=("Helvetica", 14, "bold"), text_color="white")
        self.team1_label.pack(pady=10)

        self.team2_label = ctk.CTkLabel(main_frame, text=f"Time 2: {', '.join(team2)}", font=("Helvetica", 14, "bold"), text_color="white")
        self.team2_label.pack(pady=10)

        # Labels para mostrar pontuação
        self.team1_score_label = ctk.CTkLabel(main_frame, text=f"Pontos: {self.team1_score}", font=("Helvetica", 20, "bold"), text_color="white")
        self.team1_score_label.pack(pady=5)

        self.team2_score_label = ctk.CTkLabel(main_frame, text=f"Pontos: {self.team2_score}", font=("Helvetica", 20, "bold"), text_color="white")
        self.team2_score_label.pack(pady=5)

        # Botões de adicionar ponto
        self.add_point_team1_button = ctk.CTkButton(main_frame, text="Adicionar ponto ao Time 1", command=self.add_point_team1, 
                                                    fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=200, height=40)
        self.add_point_team1_button.pack(pady=10)

        self.add_point_team2_button = ctk.CTkButton(main_frame, text="Adicionar ponto ao Time 2", command=self.add_point_team2, 
                                                    fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=200, height=40)
        self.add_point_team2_button.pack(pady=10)

    def add_point_team1(self):
        print("Ponto adicionado ao Time 1")
        self.team1_score += 1
        self.team1_score_label.configure(text=f"Pontos: {self.team1_score}")
        if self.team1_score == 12:
            self.end_match("team1")

    def add_point_team2(self):
        print("Ponto adicionado ao Time 2")
        self.team2_score += 1
        self.team2_score_label.configure(text=f"Pontos: {self.team2_score}")
        if self.team2_score == 12:
            self.end_match("team2")

    def end_match(self, winner):
        # Desabilita os botões para evitar adicionar pontos após o fim da partida
        self.add_point_team1_button.configure(state=tk.DISABLED)
        self.add_point_team2_button.configure(state=tk.DISABLED)

        # Pega o tournament_id associado a este match_id
        tournament_id = self.db.cursor.execute(
            "SELECT tournament_id FROM matches WHERE match_id = ?", (self.match_id,)
        ).fetchone()

        if not tournament_id:
            messagebox.showerror("Erro", "Torneio não encontrado para esta partida.")
            return

        tournament_id = tournament_id[0]

        # Lógica de vencedores e perdedores com perda de pontos
        if winner == "team1":
            messagebox.showinfo("Vencedor", f"Time 1 ({', '.join(self.team1)}) venceu!")
            for player in self.team1:
                player_id = self.db.cursor.execute(
                    "SELECT player_id FROM players p JOIN users u ON p.user_id = u.user_id WHERE u.name = ?",
                    (player,)
                ).fetchone()
                if player_id:
                    self.db.update_score(player_id[0], 1, self.match_id)

            # Subtrai 1 ponto do time 2
            for player in self.team2:
                player_id = self.db.cursor.execute(
                    "SELECT player_id FROM players p JOIN users u ON p.user_id = u.user_id WHERE u.name = ?",
                    (player,)
                ).fetchone()
                if player_id:
                    # Subtrai 1 ponto, mas mantém o mínimo de -1
                    self.db.update_score(player_id[0], max(-1, -1), self.match_id)

        elif winner == "team2":
            messagebox.showinfo("Vencedor", f"Time 2 ({', '.join(self.team2)}) venceu!")
            for player in self.team2:
                player_id = self.db.cursor.execute(
                    "SELECT player_id FROM players p JOIN users u ON p.user_id = u.user_id WHERE u.name = ?",
                    (player,)
                ).fetchone()
                if player_id:
                    self.db.update_score(player_id[0], 1, self.match_id)

            # Subtrai 1 ponto do time 1
            for player in self.team1:
                player_id = self.db.cursor.execute(
                    "SELECT player_id FROM players p JOIN users u ON p.user_id = u.user_id WHERE u.name = ?",
                    (player,)
                ).fetchone()
                if player_id:
                    # Subtrai 1 ponto, mas mantém o mínimo de -1
                    self.db.update_score(player_id[0], max(-1, -1), self.match_id)

        self.on_match_end()  # Chama callback para atualizar a tela anterior
        self.root.destroy()  # Fecha a janela do contador
