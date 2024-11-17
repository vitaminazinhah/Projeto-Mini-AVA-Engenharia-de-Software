import customtkinter as ctk
from PIL import Image, ImageTk
from login import show_login_screen, login, show_register_screen, register
import json


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MiniAVA(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mini AVA")
        self.geometry("800x400")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.image = Image.open("imagens/login.png")
        self.image = self.image.resize((400, 400))
        self.photo = ImageTk.PhotoImage(self.image)

       
        self.users = self.load_users()

      
        self.show_login_screen()

      
        self.students = []
    def on_closing(self):
        # Fecha todas as janelas e encerra a aplicação
        self.destroy()
    def load_users(self):
        
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {} 
        return users

    def save_users(self):

        with open("users.json", "w") as file:
            json.dump(self.users, file, indent=4)

   
    show_login_screen = show_login_screen
    login = login
    show_register_screen = show_register_screen
    register = register


app = MiniAVA()
app.mainloop()
