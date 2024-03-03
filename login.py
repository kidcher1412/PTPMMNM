import tkinter as tk
from tkinter import messagebox
import json
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firestore DB
cred = credentials.Certificate('./key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Users')

def load_user_data(username, password):
    try:
        global todo_ref
        # Check if username exists in Firestore
        user_doc = todo_ref.document(username).get()
        if user_doc.exists:
            # Check if the stored hashed password matches the input password
            stored_password = user_doc.get("password")
            if stored_password == password:
                return username
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"An Error Occurred: {e}")
        return False

def save_user_data(username, password):
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

def save_user_logined(username):
    with open("user_logined.json", "w") as file:
        json.dump({"username": username}, file)

def delete_user_logined():
    with open("user_logined.json", "w") as file:
        file.truncate()

def check_logged_in_user():
    try:
        with open("user_logined.json", "r") as file:
            data = json.load(file)
            logged_username = data.get("username", "")
            if logged_username:
                login_window.withdraw()  # Ẩn login_window nếu có ai đăng nhập
                show_main_window(logged_username)
            else:
                login_window.deiconify()  # Hiện login_window nếu không có ai đăng nhập
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        login_window.deiconify()

def login():
    username = username_entry.get()
    password = password_entry.get()
    logined_user = load_user_data(username, password)

    if logined_user:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        save_user_logined(username)
        login_window.withdraw()  # Hide the login window
        show_main_window(username)
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

def register():
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if new_username and new_password and confirm_password:
        if new_password == confirm_password:
            save_user_data(new_username, new_password)
            messagebox.showinfo(title="Registration Success", message="You successfully registered.")
            register_window.destroy()
        else:
            messagebox.showerror(title="Error", message="Passwords do not match.")
    else:
        messagebox.showerror(title="Error", message="Please fill in all fields.")

def Log_Out():
    delete_user_logined()
    main_window.destroy()  # Close the main window
    login_window.deiconify()  # Show the login window

def show_main_window(logged_username):
    global main_window
    main_window = tk.Toplevel(login_window)
    main_window.title("Main Window")
    main_window.geometry('400x300')

    label = tk.Label(main_window, text=f"Welcome, {logged_username}!", font=("Arial", 16))
    label.pack(pady=50)

    logout_button = tk.Button(main_window, text="Logout", command=Log_Out)
    logout_button.pack()

def show_register_form():
    global register_window, new_username_entry, new_password_entry, confirm_password_entry
    register_window = tk.Toplevel(login_window)
    register_window.title("Register form")
    register_window.geometry('340x440')
    register_window.configure(bg='#333333')

    new_username_label = tk.Label(register_window, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    new_username_entry = tk.Entry(register_window, font=("Arial", 16))
    new_password_label = tk.Label(register_window, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    new_password_entry = tk.Entry(register_window, show="*", font=("Arial", 16))
    confirm_password_label = tk.Label(register_window, text="Confirm Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    confirm_password_entry = tk.Entry(register_window, show="*", font=("Arial", 16))
    register_button = tk.Button(register_window, text="Register", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=register)

    new_username_label.grid(row=1, column=0)
    new_username_entry.grid(row=1, column=1, pady=20)
    new_password_label.grid(row=2, column=0)
    new_password_entry.grid(row=2, column=1, pady=20)
    confirm_password_label.grid(row=3, column=0)
    confirm_password_entry.grid(row=3, column=1, pady=20)
    register_button.grid(row=4, column=0, columnspan=2, pady=30)

# Main login form
login_window = tk.Tk()
login_window.title("Login form")
login_window.geometry('340x440')
login_window.configure(bg='#333333')

frame = tk.Frame(bg='#333333')

username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(frame, font=("Arial", 16))
password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)
register_button = tk.Button(frame, text="Register", bg="#33CC33", fg="#FFFFFF", font=("Arial", 16), command=show_register_form)

username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=10)
register_button.grid(row=4, column=0, columnspan=2, pady=10)

frame.pack()


if __name__ == "__main__":
    check_logged_in_user()  # Check if there's a logged-in user
    login_window.mainloop()  # Run the main loop

