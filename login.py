from tkinter import messagebox
import customtkinter as ctk

def login(self):
    username = self.username_entry.get()
    password = self.password_entry.get()

    if username in self.users and self.users[username] == password:
        messagebox.showinfo("Login Successful", "Welcome to the Mini AVA!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

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

    self.username_entry = ctk.CTkEntry(right_frame, placeholder_text="Username")
    self.username_entry.pack(pady=10)

    self.password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", show="*")
    self.password_entry.pack(pady=10)

    login_button = ctk.CTkButton(right_frame, text="Login", command=self.login)
    login_button.pack(pady=20)

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

    self.username_entry = ctk.CTkEntry(right_frame, placeholder_text="Username")
    self.username_entry.pack(pady=10)

    self.password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", show="*")
    self.password_entry.pack(pady=10)

    register_button = ctk.CTkButton(right_frame, text="Register", command=self.register)
    register_button.pack(pady=20)

def register(self):
    username = self.username_entry.get()
    password = self.password_entry.get()

    if username and password:
        self.users[username] = password
        messagebox.showinfo("Registration Successful", f"User {username} registered successfully!")
        self.show_login_screen()
    else:
        messagebox.showerror("Error", "Please fill out both fields.")
