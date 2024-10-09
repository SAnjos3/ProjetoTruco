import customtkinter as ctk 
from tkinter import messagebox

def start_main_app(user, login_root):
    print("Iniciando a aplicação principal...")  
    login_root.destroy()  
    root = ctk.CTk()  
    print(f"Usuário logado: {user}")  
    from gui.main_window import MainWindow  
    app = MainWindow(root, user, start_main_app)  
    root.mainloop()

if __name__ == "__main__":
    print("Iniciando a aplicação...")  
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("dark-blue")  

    root = ctk.CTk()  
    root.withdraw()  
    login_root = ctk.CTkToplevel(root)  
    print("Janela de login foi criada...")  
    from gui.login_window import LoginWindow  
    login_window = LoginWindow(login_root, lambda user: start_main_app(user, login_root))  
    login_root.mainloop()
    print("Janela de login fechada, iniciando aplicação principal...")  
