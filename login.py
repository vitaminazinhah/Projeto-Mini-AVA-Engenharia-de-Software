import customtkinter as ctk
from tkinter import messagebox
import re
import json
from menu import GoogleClassroomApp

def load_users(self):
    try:
        with open('users.json', 'r') as file:
            self.users = json.load(file)
    except FileNotFoundError:
        self.users = {}

def save_users(self):
    with open('users.json', 'w') as file:
        json.dump(self.users, file)

def login(self):
    email = self.email_entry.get()  
    password = self.password_entry.get()  

    if email in self.users and self.users[email]['password'] == password:
        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)

        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text="")

        self.withdraw()
        app = GoogleClassroomApp(self, self.users[email]['first_name'], self.users[email]['last_name'], email)
        app.mainloop()
    else:
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
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

    self.error_label = ctk.CTkLabel(right_frame, text="", font=ctk.CTkFont(size=10), text_color="red")
    self.error_label.pack(pady=5)

    new_user_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    new_user_frame.pack(pady=10)

    new_user_label = ctk.CTkLabel(new_user_frame, text="New here? ", font=ctk.CTkFont(size=12), text_color="white")
    new_user_label.pack(side="left")
    
    create_account_label = ctk.CTkLabel(new_user_frame, text="Create an account", font=ctk.CTkFont(size=12, weight="bold"), text_color="blue")
    create_account_label.pack(side="left")
    create_account_label.bind("<Button-1>", lambda e: self.show_register_screen())

# Função para mostrar a tela de registro
# Função para mostrar a tela de registro
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

    register_button = ctk.CTkButton(right_frame, text="Register", command=self.register)
    register_button.pack(pady=20)

    # Frase em negrito para voltar à tela de login
    back_to_login_label = ctk.CTkLabel(right_frame, text="Back to Login", font=ctk.CTkFont(size=12, weight="bold"), text_color="blue")
    back_to_login_label.pack(pady=10)
    back_to_login_label.bind("<Button-1>", lambda e: self.show_login_screen())



def register(self):
    first_name = self.first_name_entry.get()
    last_name = self.last_name_entry.get()
    email = self.email_entry.get()
    password = self.password_entry.get()
    confirm_password = self.confirm_password_entry.get()

    if hasattr(self, 'error_label') and self.error_label.winfo_exists():
        self.error_label.configure(text="")

    if not first_name or not last_name or not email or not password or not confirm_password:
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text="Please fill out all fields.", text_color="red")
        return

    if len(password) < 6:
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text="Password must be at least 6 characters long.", text_color="red")
        return

    if password != confirm_password:
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text="Passwords do not match.", text_color="red")
        return

    email_regex = r"(^[\w\.-]+@[\w\.-]+\.\w{2,}$)"
    if not re.match(email_regex, email):
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text="Invalid email format.", text_color="red")
        return

    if email in self.users:
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text="This email is already registered.", text_color="red")
        return

    self.users[email] = {'first_name': first_name, 'last_name': last_name, 'password': password}
    self.save_users()
    messagebox.showinfo("Registration Successful", f"User {first_name} {last_name} registered successfully!")
    self.show_login_screen()
