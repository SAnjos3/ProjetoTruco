import tkinter as tk

def on_rule_change(*args):
    print(f"Regra alterada: {rule_var.get()}")

root = tk.Tk()
root.geometry("400x200")

rule_var = tk.IntVar(value=0)  # Inicializa com 0 para garantir que uma regra seja escolhida

rule_label = tk.Label(root, text="Escolha a Regra:")
rule_label.pack(pady=5)

# Radiobuttons para selecionar as regras
rule1_radio = tk.Radiobutton(root, text="Regra 1: Sem perda de pontos ao perder", variable=rule_var, value=1)
rule1_radio.pack(pady=5)

rule2_radio = tk.Radiobutton(root, text="Regra 2: Perda de 1 ponto ao perder (mínimo -1)", variable=rule_var, value=2)
rule2_radio.pack(pady=5)

# Monitorando mudanças na variável rule_var
rule_var.trace_add("write", on_rule_change)

# Botão apenas para exibir a regra atual
def show_rule():
    print(f"Regra atual: {rule_var.get()}")

check_button = tk.Button(root, text="Verificar Regra", command=show_rule)
check_button.pack(pady=20)

root.mainloop()
