from tkcalendar import Calendar
import datetime
import customtkinter as ctk
from tkinter import messagebox

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

    agenda_window.mainloop()  # Inicia a execução do loop principal da janela de calendário
