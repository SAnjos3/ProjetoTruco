import tkinter as tk
from tkinter import messagebox
from logic.database import Database
from tournament_details_window import TournamentDetailsWindow

class EnterTournamentWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Achar Torneio")
        
        root.geometry("375x667")

        self.code_label = tk.Label(root, text="Código do Torneio:")
        self.code_label.pack(pady=5)
        self.code_entry = tk.Entry(root)
        self.code_entry.pack(pady=5)

        self.enter_button = tk.Button(root, text="Entrar no Torneio", command=self.enter_tournament)
        self.enter_button.pack(pady=20)

    def enter_tournament(self):
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
            messagebox.showinfo("Sucesso", f"Entrou no Torneio com ID {tournament_id}!")
            self.root.destroy()

            # Aqui você pode abrir a janela de detalhes do torneio ou qualquer outra ação
            tournament_details_root = tk.Toplevel(self.root)
            TournamentDetailsWindow(tournament_details_root, self.db, tournament_id)
            tournament_details_root.mainloop()
        else:
            messagebox.showerror("Erro", "Código do torneio não encontrado.")

# Exemplo de uso dessa janela (caso você precise testar separadamente)
if __name__ == "__main__":
    root = tk.Tk()
    db = Database()  # Supondo que você tenha uma classe Database implementada
    app = EnterTournamentWindow(root, db)
    root.mainloop()
