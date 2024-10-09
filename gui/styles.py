import tkinter as tk
from tkinter import ttk

def apply_styles(root):
    style = ttk.Style()

    # Tema geral
    style.theme_use('clam')

    # Estilo de Labels (escrita)
    style.configure('TLabel', 
                    font=('Helvetica', 18, 'bold'),  # Fonte negrito similar ao "Menu"
                    foreground='white',              # Texto branco
                    padding=5)

    # Definir o plano de fundo preto para a janela principal
    root.configure(bg='black')

    # Adicionar uma borda de madeira ao redor da janela
    frame = tk.Frame(root, bg="saddle brown", bd=10)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Criar um subframe com o fundo preto (a área de conteúdo)
    content = tk.Frame(frame, bg="black")
    content.pack(fill="both", expand=True, padx=10, pady=10)

    return content  # Retornar o frame onde os widgets devem ser adicionados
