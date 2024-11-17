import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import json
import random


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


class Turma:
    def __init__(self, nome, descricao="", mural=[], codigo=None):
        self.nome = nome
        self.descricao = descricao
        self.mural = mural
        self.codigo = codigo if codigo else random.randint(1000, 9999)  # Gera um código aleatório se não fornecido

    def __str__(self):
        return f"Turma: {self.nome}\nDescrição: {self.descricao}\nCódigo: {self.codigo}"

    # Método para converter a instância em um dicionário (necessário para serializar para JSON)
    def to_dict(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "codigo": self.codigo,
            "mural": self.mural
        }

    # Método de classe para criar um objeto a partir de um dicionário
    @classmethod
    def from_dict(cls, data):
        return cls(nome=data["nome"], descricao=data["descricao"], mural=data["mural"], codigo=data["codigo"])


# Lista para armazenar as turmas criadas
turmas = []

# Configurações globais
ctk.set_appearance_mode("dark")  # Opções: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"


# Função para salvar turmas em um arquivo JSON
def salvar_turmas_em_arquivo():
    try:
        with open("turmas.json", "w", encoding="utf-8") as f:
            turmas_dict = [turma.to_dict() for turma in turmas]
            json.dump(turmas_dict, f, ensure_ascii=False, indent=4)
        print("Turmas salvas com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar turmas: {e}")


# Função para carregar turmas de um arquivo JSON
def carregar_turmas_de_arquivo():
    try:
        with open("turmas.json", "r", encoding="utf-8") as f:
            turmas_dict = json.load(f)
            return [Turma.from_dict(turma) for turma in turmas_dict]
    except FileNotFoundError:
        return []  # Se o arquivo não existir, retorna uma lista vazia
    except Exception as e:
        print(f"Erro ao carregar turmas: {e}")
        return []


def criar_turma(root):
    """Função para criar a interface de criação de turmas."""
    def salvar_turma():
        """Função interna para salvar a turma."""
        nome_turma = entry_nome.get().strip()
        descricao_turma = entry_descricao.get("1.0", "end-1c").strip()

        if nome_turma:
            nova_turma = Turma(nome_turma, descricao_turma)  # Cria a nova turma
            turmas.append(nova_turma)  # Adiciona a turma à lista
            salvar_turmas_em_arquivo()  # Salva as turmas no arquivo JSON

            # Atualiza a lista de turmas na tela inicial
            atualizar_lista_turmas()

            messagebox.showinfo("Sucesso", f"Turma '{nome_turma}' criada com sucesso!")
            app.destroy()  # Fecha a tela de criação de turmas
        else:
            messagebox.showerror("Erro", "O campo 'Nome da Turma' é obrigatório!")

    # Configuração da janela principal de criação de turma
    app = ctk.CTkToplevel(root)  # Usando Toplevel para criar uma nova janela
    app.geometry("500x400")
    app.title("Criar Turma")

    # Título
    label_titulo = ctk.CTkLabel(app, text="Criar Nova Turma", font=("Arial", 24, "bold"))
    label_titulo.pack(pady=20)

    # Campo para o nome da turma
    label_nome = ctk.CTkLabel(app, text="Nome da Turma:", font=("Arial", 14))
    label_nome.pack(anchor="w", padx=20)

    entry_nome = ctk.CTkEntry(app, placeholder_text="Digite o nome da turma")
    entry_nome.pack(fill="x", padx=20, pady=5)

    # Campo para a descrição da turma
    label_descricao = ctk.CTkLabel(app, text="Descrição (opcional):", font=("Arial", 14))
    label_descricao.pack(anchor="w", padx=20)

    entry_descricao = ctk.CTkTextbox(app, height=100)
    entry_descricao.pack(fill="x", padx=20, pady=5)

    # Botão para salvar
    button_salvar = ctk.CTkButton(app, text="Salvar Turma", command=salvar_turma)
    button_salvar.pack(pady=20)

    # Rodar a aplicação
    app.mainloop()


def mostrar_detalhes_turma(turma):
    def apagar_turma():
        if messagebox.askyesno("Confirmar", f"Você tem certeza que deseja apagar a turma '{turma.nome}'?"):
            turmas.remove(turma)  # Remove a turma da lista
            salvar_turmas_em_arquivo()  # Salva as turmas restantes no arquivo JSON
            messagebox.showinfo("Sucesso", f"A turma '{turma.nome}' foi apagada com sucesso!")
            app.destroy()  # Fecha a janela de detalhes
            atualizar_lista_turmas()  # Atualiza a lista de turmas na tela inicial

    def fazer_postagem():
        def salvar_postagem():
            postagem = entry_postagem.get("1.0", "end-1c").strip()
            if postagem:
                turma.mural.append(postagem)  # Adiciona a postagem ao mural
                salvar_turmas_em_arquivo()  # Salva as turmas no arquivo JSON
                messagebox.showinfo("Sucesso", "Postagem adicionada ao mural!")
                atualizar_mural()  # Atualiza o mural na janela de detalhes
                app_postagem.destroy()  # Fecha a janela de postagem
            else:
                messagebox.showerror("Erro", "A postagem não pode estar vazia!")

        # Janela para adicionar a postagem
        app_postagem = ctk.CTkToplevel(app)
        app_postagem.geometry("400x300")
        app_postagem.title("Adicionar Postagem")

        label_postagem = ctk.CTkLabel(app_postagem, text="Digite sua postagem:", font=("Arial", 14))
        label_postagem.pack(pady=10)

        entry_postagem = ctk.CTkTextbox(app_postagem, height=100)
        entry_postagem.pack(fill="x", padx=20, pady=5)

        button_salvar_postagem = ctk.CTkButton(app_postagem, text="Adicionar Postagem", command=salvar_postagem)
        button_salvar_postagem.pack(pady=20)

    def atualizar_mural():
        label_mural_text.configure(text="\n".join(turma.mural))  # Atualiza o texto do mural

    # Configuração da janela de detalhes da turma
    app = ctk.CTk()  # Nova janela para exibir detalhes da turma
    app.geometry("500x500")
    app.title(f"Detalhes da Turma: {turma.nome}")

    # Título
    label_titulo = ctk.CTkLabel(app, text=f"Turma: {turma.nome} - Código: {turma.codigo}", font=("Arial", 24, "bold"))
    label_titulo.pack(pady=20)

    # Descrição
    label_descricao = ctk.CTkLabel(app, text="Descrição:", font=("Arial", 14))
    label_descricao.pack(anchor="w", padx=20)
    label_descricao_text = ctk.CTkLabel(app, text=turma.descricao if turma.descricao else "Sem descrição", font=("Arial", 12))
    label_descricao_text.pack(anchor="w", padx=20, pady=5)

    # Mural
    label_mural = ctk.CTkLabel(app, text="Mural:", font=("Arial", 14))
    label_mural.pack(anchor="w", padx=20)
    label_mural_text = ctk.CTkLabel(app, text="\n".join(turma.mural), font=("Arial", 12))
    label_mural_text.pack(anchor="w", padx=20, pady=5)

    button_postagem = ctk.CTkButton(app, text="Adicionar Postagem", command=fazer_postagem)
    button_postagem.pack(pady=10)

    # Botão para apagar a turma - VERMELHO e na parte inferior
    button_apagar = ctk.CTkButton(app, text="Apagar Turma", command=apagar_turma, fg_color="red")
    button_apagar.pack(side="bottom", pady=20)  # Posiciona na parte inferior com um espaçamento de 20

    app.mainloop()


def atualizar_lista_turmas():
    """Atualiza a lista de turmas na tela inicial, criando um botão para cada turma."""
    for widget in frame_turmas.winfo_children():
        widget.destroy()  # Remove todos os widgets existentes

    for turma in turmas:
        button_turma = ctk.CTkButton(frame_turmas, text=turma.nome, command=lambda turma=turma: mostrar_detalhes_turma(turma))
        button_turma.pack(fill="x", padx=20, pady=5)


def tela_inicial():
    """Tela inicial com a lista de turmas e o botão 'Criar Turma'."""
    global frame_turmas
    turmas.extend(carregar_turmas_de_arquivo())  # Carrega turmas do arquivo JSON

    # Configuração da janela inicial
    root = ctk.CTk()
    root.geometry("400x500")
    root.title("Tela Inicial")

    # Título
    label_titulo = ctk.CTkLabel(root, text="Suas Turmas:", font=("Arial", 24, "bold"))
    label_titulo.pack(pady=30)

    # Frame para os botões das turmas
    frame_turmas = ctk.CTkFrame(root)
    frame_turmas.pack(fill="both", padx=20, pady=5, expand=True)

    # Atualiza a lista de turmas
    atualizar_lista_turmas()

    # Botão para criar nova turma
    button_criar_turma = ctk.CTkButton(root, text="Criar Turma", command=lambda: criar_turma(root))
    button_criar_turma.pack(pady=20)

    # Rodar a aplicação
    root.mainloop()


# Testando a tela inicial
if __name__ == "__main__":
    tela_inicial()
