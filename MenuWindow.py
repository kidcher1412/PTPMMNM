import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class MenuWindow:
    def __init__(self, login_page, username):
        self.login_page = login_page
        self.username = username  # Lưu giữ tên người dùng
        self.main_window = None  # Khởi tạo main_window

    def menuwindow(self):
        self.main_window = tk.Toplevel()
        self.main_window.title("Menu Window")
        self.main_window.geometry('900x600')

        self.bg_frame = Image.open(r'images/backgrounds4.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.main_window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        self.menu_label = Label(self.main_window, text="MAIN MENU", bg="#A0522A", fg="#000000",
                                    font=("Arial", 25, "bold"))
        self.menu_label.place(x=380, y=80)

        #============Set background item==================
        self.menu_item = Image.open(r'images/label_item.png')
        self.photo = ImageTk.PhotoImage(self.menu_item)
        width, height = self.menu_item.size
        #==================Playonline==========================
        self.playol_button = Button(self.main_window, text='Play Online', font=("Arial", 15, "bold"), borderwidth=2,background='#A0522A',
                                   highlightthickness=0, cursor='hand2', fg='white', command=self.start)
        self.playol_button.config(image=self.photo, compound="center",width=width, height=height ) # Set image as button background and center text
        self.playol_button.place(x=400, y=180)
        #==================PlayOffline==========================
        self.playof_button = Button(self.main_window, text='Play Offline', font=("Arial", 15, "bold"), borderwidth=2,background='#A0522A',
                                   highlightthickness=0, cursor='hand2', fg='white', command=self.start)
        self.playof_button.config(image=self.photo, compound="center",width=width, height=height ) # Set image as button background and center text
        self.playof_button.place(x=400, y=280)
        #==================Log out==========================
        self.logout_button = Button(self.main_window, text='Log out', font=("Arial", 15, "bold"), borderwidth=2,background='#A0522A',
                                   highlightthickness=0, cursor='hand2', fg='white', command=self.log_out)
        self.logout_button.config(image=self.photo, compound="center",width=width, height=height ) # Set image as button background and center text
        self.logout_button.place(x=400, y=380)


        self.user_label = Label(self.main_window, text=f"Welcome, {self.username}!", font=("Arial", 16))
        self.user_label.place(x=600, y=0)
        


        

    def start():
        pass


    def log_out(self):
        self.login_page.delete_user_logined()
        if self.main_window:
            self.main_window.destroy()
        self.login_page.window.deiconify()

    def open_menu_window(self):
      self.menuwindow()
