from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import json
import time
from firebase_admin import credentials, firestore, initialize_app
from MenuWindow import MenuWindow
from RegiserWindow import RegisterWindow



#==================Init FireBase=======================
cred = credentials.Certificate('./key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Users')

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1266x800')
        self.window.resizable(0, 0)
        self.window.title('Login Page')
        # ============================background image============================

        self.bg_frame = Image.open(r'images/background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
         # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#ffffff', width=950, height=650)
        self.lgn_frame.place(x=200, y=70)
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=("Arial", 25, "bold"), bg="#ffffff",
                             fg='#000000',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ============ Left Side Image ================================================

        self.side_image = Image.open(r'images/vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ============ Sign In Image =============================================

        self.sign_in_image = Image.open(r'images/hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ============ Sign In label =============================================

        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#ffffff", fg="white",
                                    font=("Arial", 13, "bold"))
        self.sign_in_label.place(x=660, y=240)

        # ============================username====================================

        self.username_label = Label(self.lgn_frame, text="Username", bg="#ffffff", fg="#4f4e4d",
                                    font=("Arial", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#6b6a69",
                                    font=("Arial ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open(r'images/username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ============================login button================================

        self.lgn_button = Image.open(r'images/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=480)
        
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("Arial", 13, "bold"), width=24, borderwidth=0,
                    highlightthickness=0, bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.login)

        self.login.place(x=21, y=12)


        # ============================Forgot password=============================

        # self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
        #                             font=("Arial", 13, "bold underline"), fg="#000000", relief=FLAT,highlightthickness=0,
        #                             activebackground="#ffffff"
        #                             , borderwidth=0, background="#ffffff", cursor="hand2")
        # self.forgot_button.place(x=600, y=510)

        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("Arial", 13, "bold"),
                                relief=FLAT, borderwidth=0, background="#ffffff", fg='#000000')
        self.sign_label.place(x=550, y=560)

        self.signup_img = ImageTk.PhotoImage(file='images/register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",highlightthickness=0,
                                          borderwidth=0, background="#ffffff", activebackground="#ffffff",command=self.register)
        self.signup_button_label.place(x=700, y=555, width=120, height=35)

        # ============================password====================================

        self.password_label = Label(self.lgn_frame, text="Password", bg="#ffffff", fg="#4f4e4d",
                                    font=("Arial", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#6b6a69",
                                    font=("Arial", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================================================
        self.password_icon = Image.open(r'images/password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ============================================
        self.show_image = ImageTk.PhotoImage \
            (file='images/show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images/hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show_hide_password, relief=FLAT,
                              activebackground="white", borderwidth=0, background="white", cursor="hand2")

        self.show_button.place(x=860, y=420)

    def show_hide_password(self):
        if self.password_entry.cget("show") == "":
            # Nếu mật khẩu đang được hiển thị, ẩn nó và thay đổi hình ảnh của nút
            self.password_entry.config(show="*")
            self.show_button.config(image=self.show_image)
        else:
            # Nếu mật khẩu đang bị ẩn, hiển thị nó và thay đổi hình ảnh của nút
            self.password_entry.config(show="")
            self.show_button.config(image=self.hide_image)


    #==================open menu window=======================
    def open_menu_window(self):
        self.menu_window = MenuWindow(self, self.username)  # Truyền username từ LoginPage sang MenuWindow
        self.menu_window.menuwindow()



    def register(self):
        self.window.withdraw() 
        self.open_register_window()

     #==================open register window=======================
    def open_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.registerwindow(self)

    #==================Check login=======================
    def load_user_data(self, username, password):
        try:
            global todo_ref
        # Check if username exists in Firestore
            self.user_doc = todo_ref.document(username).get()
            if self.user_doc.exists:
            # Check if the stored hashed password matches the input password
                self.stored_password = self.user_doc.get("password")
                if self.stored_password == password:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"An Error Occurred: {e}")
            return False
     #==================Save User Logined=======================   
    def save_user_logined(self, username, expiration_time):
        with open("user_logined.json", "w") as file:
            json.dump({"username": username, "expiration_time": expiration_time}, file)
    #==================Delete User Logined=======================
    def delete_user_logined(self):
        with open("user_logined.json", "w") as file:
            file.truncate()

    #==================Login =======================
    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.logined_user = self.load_user_data(self.username, self.password)

        if self.logined_user:
            messagebox.showinfo(title="Login Success", message="You successfully logged in.")
            self.expiration_time = int(time.time()) + 60  # Hết hạn sau 1 phút
            self.save_user_logined(self.username, self.expiration_time)
            self.window.withdraw() 
            self.open_menu_window()
        else:
            messagebox.showerror(title="Error", message="Invalid login.")

    
    #=============save accounnt==========
    def save_user_data(self,username, password):
        try:
            global todo_ref

            export_json = {
                "username": username,
                "password": password
            }
            todo_ref.document(username).set(export_json)
            return True
        except Exception as e:
            print(f"An Error Occurred: {e}")
            return False
    #=================check login user=============
    def check_logged_in_user(self, menu_window):
        try:
            with open("user_logined.json", "r") as file:
                data = json.load(file)
                logged_username = data.get("username", "")
                if logged_username:
                    expiration_time = data.get("expiration_time", 0)
                    current_time = int(time.time())
                    if current_time < expiration_time:
                        self.window.withdraw()
                        menu_window.open_menu_window()  # Sửa lại thành menu_window.open_menu_window()
                    else:
                        messagebox.showwarning("Session Expired", "Your session has expired. Please log in again.")
                        menu_window.log_out()  # Tự động đăng xuất nếu cookie đã hết hạn
                        self.window.deiconify()  # Hiển thị lại cửa sổ đăng nhập
                else:
                    self.window.deiconify()
        except (FileNotFoundError, json.decoder.JSONDecodeError, NameError):
            self.window.deiconify()


def page():
    window = tk.Tk()
    login_page = LoginPage(window)
    
    menu_window = MenuWindow(login_page, "")  # Chuyển tham chiếu của LoginPage và username vào MenuWindow
    login_page.check_logged_in_user(menu_window)
    window.mainloop()

if __name__ == '__main__':
    page()
