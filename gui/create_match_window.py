import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from logic.match import Match
from logic.database import Database
from gui.match_counter_window import MatchCounterWindow

class CreateMatchWindow:
    def __init__(self, root, db, tournament_id, on_match_created, on_back):
        self.root = root
        self.db = db
        self.tournament_id = tournament_id
        self.on_match_created = on_match_created  # Função chamada após criar partida
        self.on_back = on_back  # Função chamada quando "Voltar" é pressionado
        self.root.title("Criar Partida")

        # Ajuste do tamanho da janela
        root.geometry("375x667")
        root.resizable(False, False)

        # Estilização da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#121212")  # Define o fundo da janela como preto mais claro

        # Inicializando as listas de times
        self.selected_team1 = []
        self.selected_team2 = []
        self.team1_confirmed = False
        self.team2_confirmed = False

        # Inicializando a lista de jogadores
        self.players = self.get_players()

        if not self.players:
            return  # Sai da função se não houver jogadores

        # Frame principal
        main_frame = ctk.CTkFrame(root, fg_color="#121212", corner_radius=0)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Label para a seleção de Time 1
        self.team1_label = ctk.CTkLabel(main_frame, text="Selecione os Jogadores do Time 1:", font=("Helvetica", 14, "bold"), text_color="white")
        self.team1_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Listbox para Time 1
        self.team1_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=8, fg="white", bg="black", font=("Helvetica", 12), highlightthickness=0, borderwidth=0)
        self.populate_listbox(self.team1_listbox, self.players)
        self.team1_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Botão para confirmar a seleção de jogadores para Time 1
        self.confirm_team1_button = ctk.CTkButton(main_frame, text="Confirmar Time 1", command=self.confirm_team1_selection,
                                                  fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=150, height=40)
        self.confirm_team1_button.grid(row=2, column=0, pady=10)

        # Label para a seleção de Time 2
        self.team2_label = ctk.CTkLabel(main_frame, text="Selecione os Jogadores do Time 2:", font=("Helvetica", 14, "bold"), text_color="white")
        self.team2_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Listbox para Time 2
        self.team2_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=8, fg="white", bg="black", font=("Helvetica", 12), highlightthickness=0, borderwidth=0)
        self.populate_listbox(self.team2_listbox, self.players)
        self.team2_listbox.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        # Botão para confirmar a seleção de jogadores para Time 2
        self.confirm_team2_button = ctk.CTkButton(main_frame, text="Confirmar Time 2", command=self.confirm_team2_selection,
                                                  fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=150, height=40)
        self.confirm_team2_button.grid(row=5, column=0, pady=10)

        # Botão para criar partida
        self.create_button = ctk.CTkButton(main_frame, text="Criar", command=self.create_match,
                                           fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=300, height=40)
        self.create_button.grid(row=6, column=0, pady=20)

        # Botão para voltar
        self.back_button = ctk.CTkButton(main_frame, text="Voltar", command=self.on_back_pressed,
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=300, height=40)
        self.back_button.grid(row=7, column=0, pady=10)

        # Configuração para expandir os listboxes
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)

    def get_players(self):
        players = self.db.cursor.execute('''
            SELECT DISTINCT u.name 
            FROM users u
            JOIN players p ON u.user_id = p.user_id
            JOIN match_players mp ON p.player_id = mp.player_id
            WHERE mp.tournament_id = ?
        ''', (self.tournament_id,)).fetchall()

        if not players:
            messagebox.showerror("Erro", "Nenhum jogador encontrado neste torneio.")
            return []

        return [player[0] for player in players]

    def populate_listbox(self, listbox, players):
        listbox.delete(0, tk.END)
        for player in players:
            listbox.insert(tk.END, player)

    def confirm_team1_selection(self):
        if self.team1_confirmed:
            self.team1_listbox.config(state=tk.NORMAL)
            self.confirm_team1_button.configure(text="Confirmar Time 1")
            self.team1_confirmed = False
        else:
            self.selected_team1 = [self.team1_listbox.get(i) for i in self.team1_listbox.curselection()]

            if len(self.selected_team1) != 2:
                messagebox.showerror("Erro", "Selecione exatamente dois jogadores para o Time 1.")
                return

            self.team1_listbox.config(state=tk.DISABLED)
            self.confirm_team1_button.configure(text="Alterar Time 1")
            self.team1_confirmed = True
            self.populate_listbox(self.team2_listbox, [p for p in self.players if p not in self.selected_team1])

    def confirm_team2_selection(self):
        if self.team2_confirmed:
            self.team2_listbox.config(state=tk.NORMAL)
            self.confirm_team2_button.configure(text="Confirmar Time 2")
            self.team2_confirmed = False
        else:
            self.selected_team2 = [self.team2_listbox.get(i) for i in self.team2_listbox.curselection()]

            if len(self.selected_team2) != 2:
                messagebox.showerror("Erro", "Selecione exatamente dois jogadores para o Time 2.")
                return

            self.team2_listbox.config(state=tk.DISABLED)
            self.confirm_team2_button.configure(text="Alterar Time 2")
            self.team2_confirmed = True
            self.populate_listbox(self.team1_listbox, [p for p in self.players if p not in self.selected_team2])

    def create_match(self):
        if len(self.selected_team1) != 2 or len(self.selected_team2) != 2:
            messagebox.showerror("Erro", "Selecione exatamente dois jogadores para cada time.")
            return

        if any(player in self.selected_team2 for player in self.selected_team1):
            messagebox.showerror("Erro", "Um jogador não pode ser selecionado para ambos os times.")
            return

        try:
            self.db.cursor.execute("INSERT INTO matches (tournament_id) VALUES (?)", (self.tournament_id,))
            match_id = self.db.cursor.lastrowid
            self.associate_players(match_id, self.selected_team1, self.selected_team2)

            self.root.withdraw()  # Oculta a janela atual
            counter_root = tk.Toplevel(self.root)
            counter_window = MatchCounterWindow(counter_root, self.db, match_id, self.selected_team1, self.selected_team2, self.on_counter_close)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao criar a partida: {e}")
            self.db.conn.rollback()

    def associate_players(self, match_id, team1, team2):
        for player in team1:
            player_id = self.db.cursor.execute("SELECT player_id FROM players p JOIN users u ON p.user_id = u.user_id WHERE u.name = ?", (player,)).fetchone()[0]
            self.db.cursor.execute("INSERT INTO match_players (match_id, player_id, tournament_id, score) VALUES (?, ?, ?, 0)", (match_id, player_id, self.tournament_id))

        for player in team2:
            player_id = self.db.cursor.execute("SELECT player_id FROM players p JOIN users u ON p.user_id = u.user_id WHERE u.name = ?", (player,)).fetchone()[0]
            self.db.cursor.execute("INSERT INTO match_players (match_id, player_id, tournament_id, score) VALUES (?, ?, ?, 0)", (match_id, player_id, self.tournament_id))

    def on_counter_close(self):
        self.root.deiconify()  # Reexibe a janela de criação de partidas após fechar o contador

    def on_back_pressed(self):
        self.root.withdraw()  # Oculta a janela de criação de partidas
        self.on_back()  # Reabre a tela de detalhes do torneio
