import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import subprocess
import perfil
import turmas_do_usuario as tdu
import json

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

        print(f"{self.name} {last_name} {email}")
        
        # Lista de códigos das turmas (para validação)
        self.your_classes = []
        self.class_codes = []

        self.base_color = "#333333"  # Cor base escura para botões e elementos
        self.hover_color = "#444444"  # Cor para hover
        self.background_color = "#000000"  # Cor de fundo preta
        self.create_widgets()

        self.show_classes_grid()

    def buscar_turmas_por_codigo(self):  #ISSO DAQUI É NOVO VIU 
        lista_de_turmas = tdu.carregar_turmas_de_arquivo()
        turmas_encontradas = [turma for turma in lista_de_turmas if turma.codigo in self.class_codes]
        return turmas_encontradas

    def create_widgets(self):
        # Navbar
        navbar_frame = ctk.CTkFrame(self, height=120, fg_color=self.background_color)
        navbar_frame.pack(fill="x", side="top", padx=10, pady=10)

        # Título
        title_label = ctk.CTkLabel(navbar_frame, text="Google Classroom", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title_label.pack(side="left", padx=20)

        # Painel para os botões no canto superior direito
        top_right_frame = ctk.CTkFrame(navbar_frame, fg_color=self.background_color)
        top_right_frame.pack(side="right", padx=20)

        # Frame para os botões ao lado do "+"
        buttons_frame = ctk.CTkFrame(top_right_frame, fg_color=self.background_color)
        buttons_frame.pack(side="left", padx=10)

        # Botão de Participar de Turma com ícone de "+"
        join_class_button = ctk.CTkButton(buttons_frame, text="+", width=30, height=30, command=self.show_join_class_window, fg_color=self.base_color, hover_color=self.hover_color, font=ctk.CTkFont(size=20, weight="bold"), corner_radius=15)
        join_class_button.pack(side="left", padx=10)

        # Botão de Criar Turma
        create_class_button = ctk.CTkButton(buttons_frame, text="Criar Turma", width=180, command=self.create_class, fg_color=self.base_color, hover_color=self.hover_color)
        create_class_button.pack(side="left", padx=10)

        # Botão de Agenda
        agenda_button = ctk.CTkButton(buttons_frame, text="Agenda", width=180, command=self.show_agenda, fg_color=self.base_color, hover_color=self.hover_color)
        agenda_button.pack(side="left", padx=10)

        # Botão de Perfil em formato de bola pequena
        profile_button = ctk.CTkButton(top_right_frame, text="P", width=30, height=30, command=self.show_profile, fg_color=self.base_color, hover_color=self.hover_color, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=15)
        profile_button.pack(side="left", padx=10)

        atualizar = ctk.CTkButton(top_right_frame, text="Atualizar", width=30, height=30, command=self.atualizar, fg_color=self.base_color, hover_color=self.hover_color, font=ctk.CTkFont(size=16, weight="bold"), corner_radius=15)
        atualizar.pack(side="left", padx=10)
    def atualizar(self):
        self.destroy()
        app = GoogleClassroomApp(self.parent,self.name,self.lastname,self.email)
        app.mainloop()

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
    # Carregando os dados do arquivo JSON onde o dicionário está armazenado
        with open('users.json', 'r') as file:
            data = json.load(file)

        # Acessa a lista de turmas do usuário usando o email
        user_data = data.get(self.email, {})
        self.classes = user_data.get("lista_colocadas", [])

        # Modal de visualização de turmas
        grid_frame = ctk.CTkFrame(self, fg_color=self.background_color)
        grid_frame.pack(pady=20, fill="both", expand=True)
        print(self.classes)
    # Verifica se há turmas para mostrar
        if not self.classes:
            no_classes_label = ctk.CTkLabel(grid_frame, text="Nenhuma turma cadastrada.", font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
            no_classes_label.pack(pady=20)
        else:
            # Itera pela lista de turmas e cria um retângulo (frame) para cada turma
            for i, class_code in enumerate(self.classes):
                # Carregando informações da turma pelo código
                lista_de_turmas = tdu.carregar_turmas_de_arquivo()
                print("oi")
                turma_info = next((turma for turma in lista_de_turmas if turma.codigo == class_code), None)

                if turma_info:
                    class_frame = ctk.CTkFrame(grid_frame, width=400, height=200, corner_radius=10, fg_color="#222222")
                    class_frame.grid(row=i//5, column=i%5, padx=20, pady=20)

                    # Nome da turma
                    class_name_label = ctk.CTkLabel(class_frame, text=turma_info.nome, font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
                    class_name_label.pack(pady=10)

                    # Subtítulo da turma
                    class_subtitle_label = ctk.CTkLabel(class_frame, text=turma_info.descricao, font=ctk.CTkFont(size=12), text_color="white")
                    class_subtitle_label.pack(pady=5)

                    # Professor
                    class_teacher_label = ctk.CTkLabel(class_frame, text=f"codigo: {turma_info.codigo}", font=ctk.CTkFont(size=10), text_color="white")
                    class_teacher_label.pack(pady=5)

                    # Botão para selecionar a turma
                    class_button = ctk.CTkButton(class_frame, text="Ver Conteúdo", command=lambda i=i: self.view_class_content(i), fg_color=self.base_color, hover_color=self.hover_color)
                    class_button.pack(pady=10)

    def show_home(self):
        messagebox.showinfo("Início", "Bem-vindo à plataforma Google Classroom!")

    def create_class(self):
        tdu.criar_turma(self)

    def join_class(self):
        # Exemplo de participação em turma
        messagebox.showinfo("Participar de Turma", "Você entrou na turma com sucesso!")

    def show_profile(self):
        # Exemplo de exibição do perfil do usuário
        perfil.call_perfil(self,self.parent,self.name,self.lastname,self.email)

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
        lista_de_turmas = tdu.carregar_turmas_de_arquivo()
        
        achou = 0
        codigo = int(code)

        for i in lista_de_turmas:
            if codigo == i.codigo:
                with open('users.json', 'r') as file:
                    data = json.load(file)
                data[self.email]["lista_colocadas"].append(codigo)
                with open('users.json', 'w') as file:
                    json.dump(data, file, indent=4)
                messagebox.showinfo("Sucesso, Você entrou na turma.")
                achou = 1
                window.destroy()
        if achou == 1:
            pass   
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
    app = GoogleClassroomApp(2,"pablo","munih","pablo@gmail.com")
    app.mainloop()