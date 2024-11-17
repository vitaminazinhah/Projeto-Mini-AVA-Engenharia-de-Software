import customtkinter as ctk

# Configurações globais
ctk.set_appearance_mode("dark")  # Opções: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"


class TelaPerfil:
    def __init__(self, root, nome, sobrenome, email):
        self.root = root  # Janela principal onde a tela de perfil será exibida
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email

        self.app = ctk.CTkToplevel(root)  # Cria uma nova janela
        self.app.geometry("400x350")
        self.app.title("Perfil do Usuário")

        self.criar_interface()

    def criar_interface(self):
        """Cria a interface gráfica da tela de perfil."""
        # Título da janela
        label_titulo = ctk.CTkLabel(self.app, text="Perfil do Usuário", font=("Arial", 24, "bold"))
        label_titulo.pack(pady=20)

        # Exibe o nome
        label_nome = ctk.CTkLabel(self.app, text=f"Nome: {self.nome}", font=("Arial", 14))
        label_nome.pack(anchor="w", padx=20, pady=5)

        # Exibe o sobrenome
        label_sobrenome = ctk.CTkLabel(self.app, text=f"Sobrenome: {self.sobrenome}", font=("Arial", 14))
        label_sobrenome.pack(anchor="w", padx=20, pady=5)

        # Exibe o e-mail
        label_email = ctk.CTkLabel(self.app, text=f"E-mail: {self.email}", font=("Arial", 14))
        label_email.pack(anchor="w", padx=20, pady=5)

        # Botão 'Voltar'
        button_voltar = ctk.CTkButton(self.app, text="Voltar", command=self.voltar)  # Associa a função 'voltar'
        button_voltar.pack(pady=20)

    def voltar(self):
        self.root.deiconify()
        self.app.destroy()  # Fecha a janela de perfil

def call_perfil(menu,name,last_name,email):
    menu.withdraw()
    app = TelaPerfil(menu, name,last_name,email)
    app.mainloop()
