import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import subprocess
import perfil
import turmas_do_usuario

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GoogleClassroomApp(ctk.CTk):
    def __init__(self,parent,first_name,last_name,email):
        super().__init__()
        
        self.name = first_name
        self.lastname = last_name
        self.email = email
        
        self.parent = parent

        self.title("Google Classroom")
        self.geometry("1000x600")

        # Inicia sem turmas
        self.classes = []
        
        # Lista de códigos das turmas (para validação)
        self.class_codes = {}

        self.base_color = "#333333"  # Cor base escura para botões e elementos
        self.hover_color = "#444444"  # Cor para hover
        self.background_color = "#000000"  # Cor de fundo preta
        self.create_widgets()

    def create_widgets(self):
        # Navbar
        navbar_frame = ctk.CTkFrame(self, height=60, fg_color=self.background_color)
        navbar_frame.pack(fill="x", side="top", padx=10, pady=10)

        # Botão de hambúrguer para abrir/fechar a navbar
        hamburger_button = ctk.CTkButton(navbar_frame, text="☰", width=40, height=40, command=self.toggle_menu, fg_color=self.base_color, hover_color=self.hover_color)
        hamburger_button.pack(side="left", padx=20)

        # Título
        title_label = ctk.CTkLabel(navbar_frame, text="Google Classroom", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title_label.pack(side="left", padx=20)

        # Painel lateral que ficará escondido inicialmente
        self.sidebar_frame = ctk.CTkFrame(self, width=200, height=600, fg_color=self.background_color)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar_frame.pack_forget()  # Começa escondido

        # Centralizando os botões na sidebar
        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Início", width=180, command=self.show_home, fg_color=self.base_color, hover_color=self.hover_color)
        self.home_button.pack(side="top", fill="x", pady=10)

        self.create_class_button = ctk.CTkButton(self.sidebar_frame, text="Criar Turma", width=180, command=self.create_class, fg_color=self.base_color, hover_color=self.hover_color)
        self.create_class_button.pack(side="top", fill="x", pady=10)

        self.join_class_button = ctk.CTkButton(self.sidebar_frame, text="Participar de Turma", width=180, command=self.show_join_class_window, fg_color=self.base_color, hover_color=self.hover_color)
        self.join_class_button.pack(side="top", fill="x", pady=10)

        self.profile_button = ctk.CTkButton(self.sidebar_frame, text="Perfil", width=180, command=self.show_profile, fg_color=self.base_color, hover_color=self.hover_color)
        self.profile_button.pack(side="top", fill="x", pady=10)

        # Botão Agenda
        self.agenda_button = ctk.CTkButton(self.sidebar_frame, text="Agenda", width=180, command=self.show_agenda, fg_color=self.base_color, hover_color=self.hover_color)
        self.agenda_button.pack(side="top", fill="x", pady=10)

        # Botão de Logout
        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", width=180, command=self.logout, fg_color="red", hover_color="#660000")
        self.logout_button.pack(side="top", fill="x", pady=10)

    def show_agenda(self):
        # Fecha a janela principal (ou seja, fecha a aplicação principal)
        self.withdraw()  # Isso oculta a janela principal (não destrói a aplicação)

        # Cria uma nova janela para a agenda (calendário)
        agenda_window = ctk.CTk()  # Criamos uma nova janela CTk
        agenda_window.title("Agenda")
        agenda_window.geometry("600x600")  # Aumentando o tamanho da tela do calendário

        # Exibe o título "Agenda"
        agenda_title_label = ctk.CTkLabel(agenda_window, text="Agenda do Mês", font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        agenda_title_label.pack(pady=10)

        # Obtém o mês e ano atuais
        current_date = datetime.datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        # Cria o calendário para o mês atual
        calendar = Calendar(agenda_window, selectmode='day', year=current_year, month=current_month, day=current_date.day)
        calendar.pack(padx=20, pady=20, expand=True)

        # Função para exibir o dia selecionado
        def on_date_select(event):
            selected_date = calendar.get_date()
            messagebox.showinfo("Data Selecionada", f"Você selecionou: {selected_date}")

        # Bind para mostrar a data selecionada
        calendar.bind("<<CalendarSelected>>", on_date_select)

        # Função para voltar ao menu principal
        def go_back_to_menu():
            agenda_window.destroy()  # Fecha a janela de calendário
            self.deiconify()  # Mostra novamente a janela principal

        # Botão "Voltar" para voltar ao menu principal
        back_button = ctk.CTkButton(agenda_window, text="Voltar", command=go_back_to_menu, fg_color=self.base_color, hover_color=self.hover_color)
        back_button.pack(pady=10)

        agenda_window.mainloop()

    def toggle_menu(self):
        # Alterna a visibilidade do menu lateral com animação
        if self.sidebar_frame.winfo_ismapped():
            self.sidebar_frame.pack_forget()  # Esconde
        else:
            # Exibe o painel lateral com animação
            self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)  # Mostra com animação de deslizamento

    def show_classes_grid(self):
        # Modal de visualização de turmas
        grid_frame = ctk.CTkFrame(self, fg_color=self.background_color)
        grid_frame.pack(pady=20, fill="both", expand=True)

        # Verifica se há turmas para mostrar
        if not self.classes:
            no_classes_label = ctk.CTkLabel(grid_frame, text="Nenhuma turma cadastrada.", font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
            no_classes_label.pack(pady=20)
        else:
            for i, class_info in enumerate(self.classes):
                class_frame = ctk.CTkFrame(grid_frame, width=200, height=200, corner_radius=10, fg_color="#222222")
                class_frame.grid(row=i//2, column=i%2, padx=20, pady=20)

                # Nome da turma
                class_name_label = ctk.CTkLabel(class_frame, text=class_info['name'], font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
                class_name_label.pack(pady=10)

                # Subtítulo da turma
                class_subtitle_label = ctk.CTkLabel(class_frame, text=class_info['subtitle'], font=ctk.CTkFont(size=12), text_color="white")
                class_subtitle_label.pack(pady=5)

                # Professor
                class_teacher_label = ctk.CTkLabel(class_frame, text=f"Professor: {class_info['teacher']}", font=ctk.CTkFont(size=10), text_color="white")
                class_teacher_label.pack(pady=5)

                # Botão para selecionar a turma
                class_button = ctk.CTkButton(class_frame, text="Ver Conteúdo", command=lambda i=i: self.view_class_content(i), fg_color=self.base_color, hover_color=self.hover_color)
                class_button.pack(pady=10)

    def show_home(self):
        messagebox.showinfo("Início", "Bem-vindo à plataforma Google Classroom!")

    def create_class(self):
        subprocess.run(['python', 'turmas_do_usuario.py'])

    def join_class(self):
        # Exemplo de participação em turma
        messagebox.showinfo("Participar de Turma", "Você entrou na turma com sucesso!")

    def show_profile(self):
        # Exemplo de exibição do perfil do usuário
        perfil.call_perfil(self,self.name,self.lastname,self.email)

    def show_join_class_window(self):
        # Janela para inserir código de turma
        join_window = ctk.CTkToplevel(self)
        join_window.title("Participar de Turma")
        join_window.geometry("400x200")

        join_label = ctk.CTkLabel(join_window, text="Digite o código da turma:")
        join_label.pack(pady=10)

        class_code_entry = ctk.CTkEntry(join_window, width=300, placeholder_text="Código da turma")
        class_code_entry.pack(pady=10)

        join_button = ctk.CTkButton(join_window, text="Participar", command=lambda: self.verify_class_code(class_code_entry.get(), join_window))
        join_button.pack(pady=10)

    def verify_class_code(self, code, window):
        # Verifica se o código da turma é válido
        if code in self.class_codes:
            class_index = self.class_codes[code]
            class_info = self.classes[class_index]
            messagebox.showinfo("Sucesso", f"Você entrou na turma {class_info['name']} com o código {code}.")
            window.destroy()
        else:
            messagebox.showerror("Erro", "Código de turma inválido. Tente novamente.")

    def view_class_content(self, index):
        # Exemplo de visualização do conteúdo de uma turma
        class_info = self.classes[index]
        messagebox.showinfo(f"Conteúdo da Turma: {class_info['name']}", f"Conteúdo de {class_info['name']} - {class_info['subtitle']}\nProfessor: {class_info['teacher']}")

    def logout(self):
    # Oculta a janela de logout
        self.parent.deiconify()
        self.destroy()

        


if __name__ == "__main__":
    app = GoogleClassroomApp()
    app.mainloop()
