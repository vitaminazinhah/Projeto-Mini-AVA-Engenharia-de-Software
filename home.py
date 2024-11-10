import customtkinter as ctk
from PIL import Image, ImageTk
from login import show_login_screen, login, show_register_screen, register

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MiniAVA(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mini AVA")
        self.geometry("800x400")

       
        self.image = Image.open("login.png")
        self.image = self.image.resize((400, 400))
        self.photo = ImageTk.PhotoImage(self.image)

       
        self.users = {"admin": "admin123"}

        
        self.show_login_screen()

       
        self.students = []

   
    show_login_screen = show_login_screen
    login = login
    show_register_screen = show_register_screen
    register = register


app = MiniAVA()
app.mainloop()
