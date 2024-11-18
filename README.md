
# **Projeto Mini-AVA**

Este é um sistema simples de gerenciamento de turmas, que permite criar, visualizar, postar em murais e gerenciar turmas. O projeto foi desenvolvido utilizando a biblioteca `customtkinter` para a interface gráfica.

---

## **Índice**
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Funcionalidades](#funcionalidades)
- [Licença](#licença)

---

## **Pré-requisitos**

Antes de executar o projeto, certifique-se de ter instalado:
- Python 3.8 ou superior.
- Um terminal ou IDE configurado com o Python.

---

## **Instalação**

1. Clone o repositório:
   ```bash
   git clone github.com/vitaminazinhah/Projeto-Mini-AVA-Engenharia-de-Software.git
   cd projeto-mini-ava
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate # Para Linux/Mac
   venv\Scripts\activate    # Para Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

   Caso não tenha o arquivo `requirements.txt`, instale as bibliotecas manualmente:
   ```bash
   pip install customtkinter tkcalendar pillow
   ```

---

## **Como Usar**

1. Após instalar as dependências, execute o arquivo principal(certifique-se de que o terminal está na pasta do programa):
   ```bash
   python main.py
   ```

2. O programa abrirá uma interface gráfica onde você pode:
   - criar ou entrar em uma conta
   - Criar novas turmas.
   - Postar mensagens no mural.
   - Apagar turmas.
   - Gerenciar dados de turmas.

---

## **Funcionalidades**

- **Criar turmas**: Adicione turmas com nome e descrição.
- **Gerenciar turmas**: Veja detalhes, poste no mural e exclua turmas.
- **Interface amigável**: Desenvolvida com `customtkinter` para um design moderno.
- **Persistência de dados**: As informações são salvas em um arquivo JSON.

---

## **Licença**

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT). 

---
