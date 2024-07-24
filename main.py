import tkinter as tk
from tkinter import Toplevel, Entry, Label, Button
from auth import login, register
from book_management import show_main_window, load_books_from_file

def main():
    global root, username_entry, password_entry
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기

    # 로그인 창 설정
    login_window = Toplevel(root)
    login_window.title("로그인")
    login_window.geometry("300x200")

    Label(login_window, text="아이디").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)

    Label(login_window, text="비밀번호").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)

    Button(login_window, text="로그인", command=lambda: login(username_entry, password_entry, login_window, root)).pack(pady=10)
    Button(login_window, text="회원가입", command=lambda: register(login_window)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
