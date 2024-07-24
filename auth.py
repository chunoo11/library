import tkinter as tk
from tkinter import Toplevel, Entry, Label, Button, messagebox
import csv
from book_management import show_main_window, load_books_from_file

# 사용자 정의
users = {
    'admin': {'password': 'adminpass', 'address': 'Admin Address', 'phone': '010-0000-0000', 'email': 'admin@example.com'}
}

def login(username_entry, password_entry, login_window, root):
    username = username_entry.get()
    password = password_entry.get()
    if username in users and users[username]['password'] == password:
        login_window.destroy()
        root.deiconify()
        show_main_window(root)
        load_books_from_file()
    else:
        messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")

def register(login_window):
    def submit_registration():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        if new_username in users:
            messagebox.showerror("회원가입 실패", "이미 존재하는 아이디입니다.")
        elif new_password != confirm_password:
            messagebox.showerror("회원가입 실패", "비밀번호가 일치하지 않습니다.")
        elif not new_username or not new_password or not address or not phone or not email:
            messagebox.showerror("회원가입 실패", "모든 필드를 입력해주세요.")
        else:
            users[new_username] = {'password': new_password, 'address': address, 'phone': phone, 'email': email}
            messagebox.showinfo("회원가입 성공", "회원가입이 완료되었습니다.")
            register_window.destroy()

    register_window = Toplevel(login_window)
    register_window.title("회원가입")
    register_window.geometry("300x500")

    Label(register_window, text="새 아이디").pack(pady=5)
    new_username_entry = Entry(register_window)
    new_username_entry.pack(pady=5)

    Label(register_window, text="새 비밀번호").pack(pady=5)
    new_password_entry = Entry(register_window, show="*")
    new_password_entry.pack(pady=5)

    Label(register_window, text="비밀번호 확인").pack(pady=5)
    confirm_password_entry = Entry(register_window, show="*")
    confirm_password_entry.pack(pady=5)

    Label(register_window, text="주소").pack(pady=5)
    address_entry = Entry(register_window)
    address_entry.pack(pady=5)

    Label(register_window, text="전화번호").pack(pady=5)
    phone_entry = Entry(register_window)
    phone_entry.pack(pady=5)

    Label(register_window, text="이메일").pack(pady=5)
    email_entry = Entry(register_window)
    email_entry.pack(pady=5)

    Button(register_window, text="가입", command=submit_registration).pack(pady=20)

def save_user_to_csv(username, password, address, phone, email):
    try:
        with open('users.csv', 'a', newline='') as csvfile:
            fieldnames = ['username', 'password', 'address', 'phone', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerrow({'username': username, 'password':password, 'address': address, 'phone' : phone, 'email' : email})
    except FileNotFoundError:
            pass

if __name__ == "__main__":
    load_user_form_csv()

    root = tk.Tk()
    root.withdraw()
    
    login_window = Toplevel(root)
    login_window.title("로그인")
    login_window.geometry("300x 300")

    Label(login_window, text="아이디").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)

    Label(login_window, text="비밀번호").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)

    Button(login_window, text="로그인", command=lambda: login(username_entry, password_entry, login_window, root)).pack(pady=10)
    Button(login_window, text="회원가입", command=lambda: register(login_window)).pack(pady=10)

    root.mainloop()
