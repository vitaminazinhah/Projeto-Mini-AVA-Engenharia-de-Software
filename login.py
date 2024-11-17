import customtkinter as ctk
from tkinter import messagebox
import re
from menu import GoogleClassroomApp

def login(self):
    email = self.email_entry.get()  
    password = self.password_entry.get()  

    # Verifica se o email e a senha estão corretos
    if email in self.users and self.users[email]['password'] == password:

        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)

        self.error_label.configure(text="")  # Limpar a mensagem de erro

        self.withdraw()
        app = GoogleClassroomApp(self, self.users[email]['first_name'],self.users[email]['last_name'],email)
        app.mainloop()
        
        # Limpa a mensagem de erro caso o login seja bem-sucedido
        
    else:
        # Exibe a mensagem de erro
        self.error_label.configure(text="Invalid email or password.", text_color="red")

def show_login_screen(self):
    for widget in self.winfo_children():
        widget.destroy()

    left_frame = ctk.CTkFrame(self, width=400, height=400, fg_color="white")
    left_frame.pack(side="left", fill="both", expand=True)

    label_image = ctk.CTkLabel(left_frame, image=self.photo, text="")
    label_image.pack(pady=20)

    right_frame = ctk.CTkFrame(self, width=400, height=400, fg_color="transparent")
    right_frame.pack(side="right", fill="both", expand=True)

    login_label = ctk.CTkLabel(right_frame, text="Login", font=ctk.CTkFont(size=20, weight="bold"))
    login_label.pack(pady=20)

    self.email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email")
    self.email_entry.pack(pady=10)

    self.password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", show="*")
    self.password_entry.pack(pady=10)

    login_button = ctk.CTkButton(right_frame, text="Login", command=self.login)
    login_button.pack(pady=20)

    # Novo Label para mensagem de erro
    self.error_label = ctk.CTkLabel(right_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
    self.error_label.pack(pady=5)

    new_user_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    new_user_frame.pack(pady=10)

    new_user_label = ctk.CTkLabel(new_user_frame, text="New here? ", font=ctk.CTkFont(size=12), text_color="white")
    new_user_label.pack(side="left")
    
    create_account_label = ctk.CTkLabel(new_user_frame, text="Create an account", font=ctk.CTkFont(size=12, weight="bold"), text_color="blue")
    create_account_label.pack(side="left")
    create_account_label.bind("<Button-1>", lambda e: self.show_register_screen())


def show_register_screen(self):
    for widget in self.winfo_children():
        widget.destroy()

    left_frame = ctk.CTkFrame(self, width=400, height=400, fg_color="white")
    left_frame.pack(side="left", fill="both", expand=True)

    label_image = ctk.CTkLabel(left_frame, image=self.photo, text="")
    label_image.pack(pady=20)

    right_frame = ctk.CTkFrame(self, width=400, height=400)
    right_frame.pack(side="right", fill="both", expand=True)

    register_label = ctk.CTkLabel(right_frame, text="Create an Account", font=ctk.CTkFont(size=20, weight="bold"))
    register_label.pack(pady=20)

    # Campos de entrada para nome, sobrenome, email, senha e confirmação de senha
    self.first_name_entry = ctk.CTkEntry(right_frame, placeholder_text="First Name")
    self.first_name_entry.pack(pady=10)

    self.last_name_entry = ctk.CTkEntry(right_frame, placeholder_text="Last Name")
    self.last_name_entry.pack(pady=10)

    self.email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email")
    self.email_entry.pack(pady=10)

    self.password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", show="*")
    self.password_entry.pack(pady=10)

    self.confirm_password_entry = ctk.CTkEntry(right_frame, placeholder_text="Confirm Password", show="*")
    self.confirm_password_entry.pack(pady=10)

    # Botão de registro
    register_button = ctk.CTkButton(right_frame, text="Register", command=self.register)
    register_button.pack(pady=20)

def register(self):
    # Pegando os valores dos campos de entrada
    first_name = self.first_name_entry.get()
    last_name = self.last_name_entry.get()
    email = self.email_entry.get()
    password = self.password_entry.get()
    confirm_password = self.confirm_password_entry.get()

    # Limpar a mensagem de erro anterior, se houver
    self.error_label.configure(text="")

    # Validação dos campos
    if not first_name or not last_name or not email or not password or not confirm_password:
        self.error_label.configure(text="Please fill out all fields.", text_color="red")
        return

    # Verificando se a senha tem pelo menos 6 caracteres
    if len(password) < 6:
        self.error_label.configure(text="Password must be at least 6 characters long.", text_color="red")
        return

    # Verificando se a confirmação da senha corresponde à senha
    if password != confirm_password:
        self.error_label.configure(text="Passwords do not match.", text_color="red")
        return

    # Validando o formato do e-mail
    email_regex = r"(^[\w\.-]+@[\w\.-]+\.\w{2,}$)"
    if not re.match(email_regex, email):
        self.error_label.configure(text="Invalid email format.", text_color="red")
        return

    # Verificando se o e-mail já existe no sistema
    if email in self.users:
        self.error_label.configure(text="This email is already registered.", text_color="red")
        return

    # Se tudo estiver correto, armazena o usuário e mostra mensagem de sucesso
    self.users[email] = {'first_name': first_name, 'last_name': last_name, 'password': password}
    self.save_users() 
    messagebox.showinfo("Registration Successful", f"User {first_name} {last_name} registered successfully!")
    self.show_login_screen()
