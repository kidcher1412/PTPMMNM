import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image


class RegisterWindow:
    def __init__(self, login_page):
        self.login_page = login_page
    def registerwindow(self, login_page):
        self.register_window = tk.Toplevel()
        self.register_window.title("Regiser")  
        self.register_window.geometry('1266x800')  # Adjust dimensions based on image
        self.register_window.configure(bg='#F2F2F2')  # Lighter background color    

        self.bg_frame = Image.open(r'images/background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.register_window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
         # ====== Sign up Frame =========================
        self.lgn_frame = Frame(self.register_window, bg='#ffffff', width=900, height=620)
        self.lgn_frame.place(x=200, y=70)
        # ====== Sign up Label =========================
        self.sign_in_label = Label(self.lgn_frame, text="SIGN UP", bg="#ffffff", fg="#000000",
                                    font=("Arial", 25, "bold"))
        self.sign_in_label.place(x=420, y=70)

        # =============Username label and entry=================
        self.new_username_label = Label(self.lgn_frame, text="Username", bg='#ffffff', fg="#000000", font=("Arial", 14))
        self.new_username_label.place(x=250, y=160)
        self.new_username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#6b6a69",
                                    font=("Arial ", 12, "bold"), insertbackground = '#6b6a69')
        self.new_username_entry.place(x=380, y=160, width=270)
        self.new_username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.new_username_line.place(x=350, y=184)
        # ===============Username icon=====================
        self.new_username_icon = Image.open(r'images/username_icon.png')
        photo = ImageTk.PhotoImage(self.new_username_icon)
        self.new_username_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.new_username_icon_label.image = photo
        self.new_username_icon_label.place(x=350, y=157)

        #================ Password label and entry===============
        self.new_password_label = Label(self.lgn_frame, text="Password", bg='#ffffff', fg="#000000", font=("Arial", 14))
        self.new_password_label.place(x=250, y=240)
        self.new_password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#6b6a69",
                                    font=("Arial", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.new_password_entry.place(x=380, y=240, width=270)
        self.new_password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.new_password_line.place(x=350, y=264)
        # =================Password icon======================
        self.new_password_icon = Image.open(r'images/password_icon.png')
        photo = ImageTk.PhotoImage(self.new_password_icon)
        self.new_password_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.new_password_icon_label.image = photo
        self.new_password_icon_label.place(x=350, y=237)

         #==================== confirm Password label and entry===============
        self.confirm_password_label = Label(self.lgn_frame, text="Confirm Password", bg='#ffffff', fg="#000000", font=("Arial", 14))
        self.confirm_password_label.place(x=180, y=320)
        self.confirm_password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#6b6a69",
                                    font=("Arial", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.confirm_password_entry.place(x=380, y=320, width=270)
        self.new_confirm_password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.new_confirm_password_line.place(x=350, y=344)

        # ===============confirm Password icon===================

        self.new_confirm_password_icon = Image.open(r'images/key_icon.png')
        new_width = 22
        new_height = 23
        self.new_confirm_password_icon = self.new_confirm_password_icon.resize((new_width,new_height))

        photo = ImageTk.PhotoImage(self.new_confirm_password_icon)
        self.new_confirm_password_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.new_confirm_password_icon_label.image = photo
        self.new_confirm_password_icon_label.place(x=350, y=317)
        # ==============hide and show==================
        self.show_image = ImageTk.PhotoImage \
            (file='images/show.png')
        self.hide_image = ImageTk.PhotoImage \
            (file='images/hide.png')
        self.show_button_pass = Button(self.lgn_frame, image=self.show_image, command=self.show_hide_password, relief=FLAT,
                              activebackground="white", borderwidth=0, background="white", cursor="hand2")

        self.show_button_pass.place(x=650, y=240)

        self.show_button_comfirm_pass = Button(self.lgn_frame, image=self.show_image, command=self.show_hide_comfirm_password, relief=FLAT,
                              activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button_comfirm_pass.place(x=650, y=320)

        #================ Register button====================
        self.rgt_button = Image.open(r'images/btn1.png')
        photo = ImageTk.PhotoImage(self.rgt_button)
        self.rgt_button_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.rgt_button_label.image = photo
        self.rgt_button_label.place(x=300, y=450)

        self.register_button = Button(self.rgt_button_label, text='Register', font=("Arial", 13, "bold"), width=24, borderwidth=0,
                    highlightthickness=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.register)
        self.register_button.place(x=21, y=12)

     # ===============back Login page===============
        self.signin_img = ImageTk.PhotoImage(file='images/login.png')
        self.signin_button_label = Button(self.lgn_frame, image=self.signin_img, bg='#98a65d', cursor="hand2",highlightthickness=0,
                                          borderwidth=0, background="#ffffff", activebackground="#ffffff",command=self.login_pages)
        self.signin_button_label.place(x=650, y=450, width=64, height=64)

    # ==============hide and show==============================
    def show_hide_password(self):
        if self.new_password_entry.cget("show") == "":
            self.new_password_entry.config(show="*")
            self.show_button_pass.config(image=self.show_image)
        else:
            self.new_password_entry.config(show="")
            self.show_button_pass.config(image=self.hide_image)
    def show_hide_comfirm_password(self):
        if self.confirm_password_entry.cget("show") == "":
            self.confirm_password_entry.config(show="*")
            self.show_button_comfirm_pass.config(image=self.show_image)
        else:
            self.confirm_password_entry.config(show="")
            self.show_button_comfirm_pass.config(image=self.hide_image)

    def login_pages(self):  
        if self.register_window:
            self.register_window.destroy()
            self.login_page.window.deiconify() 

    def register(self):
        self.new_username = self.new_username_entry.get()
        self.new_password = self.new_password_entry.get()
        self.confirm_password = self.confirm_password_entry.get()

        if self.new_username and self.new_password and self.confirm_password:
            if self.new_password == self.confirm_password:
                self.login_page.save_user_data(self.new_username, self.new_password)
                messagebox.showinfo(title="Registration Success", message="You successfully registered.")
                if self.register_window:
                    self.register_window.destroy()
                    self.login_page.window.deiconify()
         

            else:
                messagebox.showerror(title="Error", message="Passwords do not match.")
        else:
            messagebox.showerror(title="Error", message="Please fill in all fields.")
   