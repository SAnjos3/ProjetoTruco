import customtkinter as ctk
from tkinter import messagebox
from logic.database import Database
from gui.create_tournament_window import CreateTournamentWindow
from gui.find_tournament_window import FindTournamentWindow
from gui.view_tournaments import ViewTournamentsWindow
from gui.tournament_details_window import TournamentDetailsWindow
from gui.login_window import LoginWindow

class MainWindow:
    def __init__(self, root, user, start_main_app):
        self.root = root
        self.user = user
        self.db = Database()
        self.start_main_app = start_main_app

        # Desativar animações
        ctk.disable_animations = True

        # Armazena o ID de qualquer evento 'after' ativo
        self.after_id = None

        # Configurações da janela principal
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        root.geometry("375x667")
        root.configure(bg="black")

        # Estado do menu
        self.menu_open_state = [False]

        # Botão de três traços (menu hamburguer)
        self.menu_button = ctk.CTkButton(root, text="☰", command=self.toggle_menu,
                                         fg_color="black", text_color="white", hover_color="brown", corner_radius=10, border_width=2, border_color="brown")
        self.menu_button.place(x=10, y=10)

        # Menu lateral com fundo marrom
        self.side_menu = ctk.CTkFrame(root, fg_color="#8B4513", width=200, height=667, corner_radius=10)
        self.side_menu.place_forget()

        # Botão de perfil no menu lateral
        profile_button = ctk.CTkButton(self.side_menu, text="Perfil", command=self.show_profile,
                                       fg_color="black", text_color="white", hover_color="brown", corner_radius=10, border_width=2, border_color="brown")
        profile_button.pack(pady=10)

        # Botão de logout no menu lateral
        logout_button = ctk.CTkButton(self.side_menu, text="Logout", command=self.logout,
                                      fg_color="black", text_color="white", hover_color="brown", corner_radius=10, border_width=2, border_color="brown")
        logout_button.pack(pady=10)

        # Botão "X" para fechar o menu
        self.x_button = ctk.CTkButton(self.side_menu, text="X", command=self.close_menu,
                                      fg_color="black", text_color="white", hover_color="brown", corner_radius=10, border_width=2, border_color="brown")
        self.x_button.pack(pady=10)

        # Botão de ação
        self.button_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.button_frame.pack(expand=True)

        # Botão para visualizar torneios
        self.view_tournaments_button = ctk.CTkButton(self.button_frame, text="Ver Torneios", command=self.view_tournaments,
                                                     fg_color="black", text_color="white", hover_color="brown",
                                                     corner_radius=10, border_width=2, border_color="brown",
                                                     width=150, height=50)
        self.view_tournaments_button.pack(pady=50)

    def toggle_menu(self):
        if self.menu_open_state[0]:
            self.side_menu.place_forget()
            self.menu_open_state[0] = False
        else:
            self.side_menu.place(x=0, y=0)
            self.menu_open_state[0] = True

    def close_menu(self):
        self.side_menu.place_forget()
        self.menu_open_state[0] = False

    def on_closing(self):
        try:
            if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
                # Cancela qualquer evento 'after' ativo antes de fechar
                if self.after_id:
                    self.root.after_cancel(self.after_id)
                self.db.close()  # Fechar a conexão com o banco de dados
                self.root.quit()
                self.root.destroy()
        except Exception as e:
            print(f"Erro ao tentar fechar: {e}")
            self.root.quit()

    def view_tournaments(self):
        # Cancela qualquer evento 'after' ativo antes de fechar
        if self.after_id:
            self.root.after_cancel(self.after_id)
        # Fecha a janela principal e abre a janela de torneios
        self.root.withdraw()  # Alterado para ocultar a janela principal ao invés de destruí-la
        view_tournaments_root = ctk.CTk()
        view_tournaments_window = ViewTournamentsWindow(view_tournaments_root, self.db, self.user, self.back_to_main)
        view_tournaments_root.geometry("375x667")
        view_tournaments_root.mainloop()
        self.root.deiconify()  # Reexibe a janela principal ao fechar a janela de torneios

    def back_to_main(self):
        self.root.deiconify()  # Reexibe a janela principal quando voltar

    def show_profile(self):
        profile_window = ctk.CTkToplevel(self.root)
        profile_window.title("Perfil")
        profile_window.geometry("375x667")
        profile_window.configure(bg="black")

        username_label = ctk.CTkLabel(profile_window, text=f"Usuário: {self.user[1]}", text_color="white", font=("Helvetica", 12))
        email_label = ctk.CTkLabel(profile_window, text=f"Email: {self.user[2]}", text_color="white", font=("Helvetica", 12))

        username_label.pack(pady=10)
        email_label.pack(pady=10)

    def logout(self):
        # Cancela qualquer evento 'after' ativo antes de fechar
        if self.after_id:
            self.root.after_cancel(self.after_id)
        messagebox.showinfo("Logout", "Você foi desconectado.")
        self.root.destroy()
        login_root = ctk.CTk()
        login_window = LoginWindow(login_root, on_success=lambda user: self.start_main_app(user, login_root))
        login_root.mainloop()
