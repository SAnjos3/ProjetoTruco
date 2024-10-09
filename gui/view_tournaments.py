import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from gui.create_tournament_window import CreateTournamentWindow
from gui.find_tournament_window import FindTournamentWindow
from gui.tournament_details_window import TournamentDetailsWindow
import sqlite3

class ViewTournamentsWindow:
    def __init__(self, root, db, user, on_back):
        self.root = root
        self.db = db
        self.user = user
        self.on_back = on_back
        self.root.title("Torneios")

        # Estilizando a janela principal
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Desabilitar animações para evitar erros de click_animation
        ctk.disable_animations = True

        # Título
        self.title_label = ctk.CTkLabel(root, text="Torneios", font=("Helvetica", 20, "bold"), text_color="white")
        self.title_label.pack(pady=20)

        # Listbox para mostrar os torneios
        self.tournaments_listbox = ctk.CTkFrame(root, fg_color="black", corner_radius=10, width=300, height=250)
        self.listbox_inner = tk.Listbox(self.tournaments_listbox, fg="white", bg="black", font=("Helvetica", 12), 
                                        selectbackground="brown", highlightthickness=0, borderwidth=0)  # Removed borders
        self.listbox_inner.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tournaments_listbox.pack(pady=10, padx=10)

        # Exibir apenas os torneios criados ou onde o usuário está inscrito
        self.refresh_tournaments()

        # Botão para criar novo torneio
        self.create_tournament_button = ctk.CTkButton(root, text="Criar Novo Torneio", command=self.open_create_tournament_window,
                                                      fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", 
                                                      width=200, height=40)
        self.create_tournament_button.pack(pady=10)

        # Botão para achar torneio existente
        self.find_tournament_button = ctk.CTkButton(root, text="Achar Torneio", command=self.open_find_tournament_window,
                                                    fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", 
                                                    width=200, height=40)
        self.find_tournament_button.pack(pady=10)

        # Botão para ver detalhes do torneio
        self.details_button = ctk.CTkButton(root, text="Ver Detalhes", command=self.show_tournament_details,
                                            fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", 
                                            width=200, height=40)
        self.details_button.pack(pady=10)

        # Botão para deletar torneio
        self.delete_button = ctk.CTkButton(root, text="Deletar Torneio", command=self.delete_tournament,
                                           fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", 
                                           width=200, height=40)
        self.delete_button.pack(pady=10)

        # Botão para voltar à janela principal
        self.back_button = ctk.CTkButton(root, text="Voltar", command=self.go_back,
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=15, border_width=2, border_color="brown", 
                                         width=200, height=40)
        self.back_button.pack(pady=20)

        # Agora que a interface foi configurada, defina a geometria e atualize a janela
        self.root.geometry("375x667")  # Ajuste correto para o tamanho de celular
        self.root.resizable(False, False)  # Impede o redimensionamento
        self.root.update_idletasks()  # Força a atualização do layout da janela

    def open_create_tournament_window(self):
        # Fecha a janela atual de view tournaments
        self.root.withdraw()
        
        # Cria e abre a janela de criar torneio
        create_tournament_root = ctk.CTk()  # Abre uma nova janela para criar torneio
        create_tournament_root.geometry("375x667")  # Garante o tamanho da nova janela
        create_tournament_root.resizable(False, False)  # Impede o redimensionamento
        CreateTournamentWindow(create_tournament_root, self.db, self.refresh_tournaments, self.user, self.root.deiconify)
        create_tournament_root.mainloop()

    def open_find_tournament_window(self):
        self.root.withdraw()  # Esconde a janela atual
        find_tournament_root = ctk.CTk()  # Abre uma nova janela para encontrar torneio
        find_tournament_root.geometry("375x667")  # Garante o tamanho da nova janela
        find_tournament_root.resizable(False, False)  # Impede o redimensionamento
        FindTournamentWindow(find_tournament_root, self.db, self.refresh_tournaments, self.user, self.back_to_tournaments)
        find_tournament_root.mainloop()
        self.root.deiconify()  # Reexibe a janela de torneios ao fechar a janela de achar torneio

    def refresh_tournaments(self):
        # Verifica se o Listbox ainda existe antes de tentar manipulá-lo
        if self.listbox_inner.winfo_exists():
            # Atualiza a lista de torneios
            self.listbox_inner.delete(0, tk.END)

            tournaments = self.db.cursor.execute('''
                SELECT DISTINCT t.name 
                FROM tournaments t
                LEFT JOIN match_players mp ON t.tournament_id = mp.tournament_id
                LEFT JOIN players p ON mp.player_id = p.player_id
                LEFT JOIN users u ON u.user_id = p.user_id
                WHERE u.user_id = ? OR t.creator_user_id = ?
            ''', (self.user[0], self.user[0])).fetchall()

            for tournament in tournaments:
                self.listbox_inner.insert(tk.END, tournament[0])
        else:
            print("O Listbox foi destruído ou não está mais disponível.")

    def show_tournament_details(self):
        selected_index = self.listbox_inner.curselection()
        if selected_index:
            tournament_name = self.listbox_inner.get(selected_index)
            tournament_id = self.db.cursor.execute("SELECT tournament_id FROM tournaments WHERE name = ?", (tournament_name,)).fetchone()

            if tournament_id:
                self.root.withdraw()  # Esconde a janela atual
                tournament_details_root = ctk.CTk()  # Abre uma nova janela para os detalhes do torneio
                tournament_details_root.geometry("375x667")  # Garante o tamanho da nova janela
                tournament_details_root.resizable(False, False)  # Impede o redimensionamento
                TournamentDetailsWindow(tournament_details_root, self.db, tournament_id[0], self.back_to_tournaments)
                tournament_details_root.mainloop()
                self.root.deiconify()  # Reexibe a janela de torneios ao fechar a de detalhes
            else:
                messagebox.showerror("Erro", "Torneio não encontrado.")
        else:
            messagebox.showerror("Erro", "Selecione um torneio.")

    def delete_tournament(self):
        selected_index = self.listbox_inner.curselection()
        if selected_index:
            tournament_name = self.listbox_inner.get(selected_index)
            cursor = None
            try:
                # Use a conexão existente em vez de criar uma nova
                cursor = self.db.conn.cursor()
    
                tournament_id = cursor.execute("SELECT tournament_id, creator_user_id FROM tournaments WHERE name = ?", (tournament_name,)).fetchone()
    
                if tournament_id:
                    if tournament_id[1] == self.user[0]:  # Verifica se o usuário é o criador do torneio
                        confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o torneio \'{tournament_name}\'?")
                        if confirm:
                            # Executa a deleção e commita a operação
                            cursor.execute("BEGIN IMMEDIATE")
                            cursor.execute("DELETE FROM tournaments WHERE tournament_id = ?", (tournament_id[0],))
                            self.db.conn.commit()
                            messagebox.showinfo("Sucesso", f"Torneio \'{tournament_name}\' deletado com sucesso.")
                            self.refresh_tournaments()
                    else:
                        messagebox.showerror("Erro", "Você não tem permissão para deletar este torneio.")
                else:
                    messagebox.showerror("Erro", "Torneio não encontrado.")
    
            except sqlite3.OperationalError as e:
                messagebox.showerror("Erro", f"Erro ao deletar torneio: {e}")
            finally:
                # Certifique-se de fechar o cursor após a operação
                if cursor:
                    cursor.close()
        else:
            messagebox.showerror("Erro", "Selecione um torneio.")


    def go_back(self):
        self.root.destroy()
        self.on_back()

    def back_to_tournaments(self):
        # Função para voltar à janela de torneios
        root = ctk.CTk()
        ViewTournamentsWindow(root, self.db, self.user, self.on_back)
        root.geometry("375x667")  # Garante o tamanho da nova janela
        root.resizable(False, False)  # Impede o redimensionamento
        root.mainloop()
