import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gui.create_match_window import CreateMatchWindow
from logic.database import Database

class TournamentDetailsWindow:
    def __init__(self, root, db, tournament_id, on_back):
        self.root = root
        self.db = db
        self.tournament_id = tournament_id
        self.on_back = on_back  # Callback para voltar à janela anterior
        self.root.title("Detalhes do Torneio")
        
        # Ajuste do tamanho da janela
        root.geometry("375x667")
        root.resizable(False, False)

        # Estilização da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#121212")  # Preto mais escuro

        # Criação de um frame principal sem margem
        main_frame = ctk.CTkFrame(root, fg_color="#121212", corner_radius=0)  # Fundo preto mais escuro, sem borda
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Obter o nome e o código do torneio
        tournament_info = self.db.cursor.execute(
            "SELECT name, code FROM tournaments WHERE tournament_id = ?", (self.tournament_id,)
        ).fetchone()

        if tournament_info:
            tournament_name, tournament_code = tournament_info

            # Exibir o nome do torneio
            self.name_label = ctk.CTkLabel(main_frame, text=f"Torneio: {tournament_name}", font=("Helvetica", 16), text_color="white")
            self.name_label.grid(row=0, column=0, columnspan=2, pady=10)

            # Exibir o código do torneio
            self.code_label = ctk.CTkLabel(main_frame, text=f"Código do Torneio: {tournament_code}", font=("Helvetica", 14), text_color="white")
            self.code_label.grid(row=1, column=0, columnspan=2, pady=10)

            # Exibir os participantes do torneio
            self.participants_label = ctk.CTkLabel(main_frame, text="Participantes:", font=("Helvetica", 12), text_color="white")
            self.participants_label.grid(row=2, column=0, pady=5)

            self.participants_listbox = tk.Listbox(main_frame, bg="black", fg="white", font=("Helvetica", 12), highlightthickness=0)
            self.participants_listbox.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
            self.show_participants()

            # Botão para criar nova partida
            self.create_match_button = ctk.CTkButton(main_frame, text="Criar Partida", command=self.create_match, 
                                                     fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=150, height=40)
            self.create_match_button.grid(row=4, column=0, pady=10)

            # Lista de partidas no torneio
            self.matches_label = ctk.CTkLabel(main_frame, text="Partidas:", font=("Helvetica", 12), text_color="white")
            self.matches_label.grid(row=2, column=1, pady=5)

            self.matches_listbox = tk.Listbox(main_frame, bg="black", fg="white", font=("Helvetica", 12), highlightthickness=0)
            self.matches_listbox.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")
            self.show_matches()

            # Botão para voltar
            self.back_button = ctk.CTkButton(main_frame, text="Voltar", command=self.go_back, 
                                             fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", width=150, height=40)
            self.back_button.grid(row=5, column=0, columnspan=2, pady=20)
        else:
            messagebox.showerror("Erro", "Torneio não encontrado.")

        # Ajustes para expandir os widgets corretamente
        main_frame.grid_rowconfigure(3, weight=1)  # Expande as linhas de Listbox
        main_frame.grid_columnconfigure((0, 1), weight=1)  # Expande as colunas para os Listboxes

    def show_participants(self):
        # Limpa a listbox de participantes antes de preencher novamente
        self.participants_listbox.delete(0, tk.END)

        participants = self.db.cursor.execute('''
            SELECT u.name, SUM(mp.score)
            FROM match_players mp
            JOIN players p ON mp.player_id = p.player_id
            JOIN users u ON p.user_id = u.user_id
            WHERE mp.tournament_id = ?
            GROUP BY u.name
        ''', (self.tournament_id,)).fetchall()

        if participants:
            for participant in participants:
                self.participants_listbox.insert(tk.END, f"{participant[0]}: {participant[1]} pontos")
        else:
            self.participants_listbox.insert(tk.END, "Nenhum participante encontrado.")
            
    def show_matches(self):
        # Limpa a listbox de partidas antes de preencher novamente
        self.matches_listbox.delete(0, tk.END)

        matches = self.db.cursor.execute(
            "SELECT match_id FROM matches WHERE tournament_id = ?", (self.tournament_id,)
        ).fetchall()

        if matches:
            for match in matches:
                self.matches_listbox.insert(tk.END, f"Partida {match[0]}")
        else:
            self.matches_listbox.insert(tk.END, "Nenhuma partida encontrada.")

    def create_match(self):
        try:
            self.root.withdraw()  # Oculta a janela atual

            # Criar nova janela para criar partida
            create_match_root = tk.Toplevel(self.root)
            
            # Passando 'on_back' para voltar corretamente para os detalhes do torneio
            create_match_window = CreateMatchWindow(create_match_root, self.db, self.tournament_id, self.show_matches, self.on_back)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar partida: {e}")

    def cancel_animations(self):
        """Cancela qualquer animação pendente ou chamada after"""
        if hasattr(self, 'create_match_button'):
            try:
                self.create_match_button.after_cancel(self.create_match_button)  # Cancela a animação do botão
            except:
                pass
        if hasattr(self, 'back_button'):
            try:
                self.back_button.after_cancel(self.back_button)  # Cancela a animação do botão 'voltar'
            except:
                pass

    def go_back(self):
        # Cancela animações antes de destruir a janela
        self.cancel_animations()

        if self.root.winfo_exists():
            self.root.destroy()  # Destroi a janela atual
        self.on_back()  # Reabre a tela de detalhes do torneio
