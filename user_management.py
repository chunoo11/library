import tkinter as tk
from tkinter import Toplevel, Entry, Label, Button, messagebox

users = {
    'admin': {'password': 'adminpass', 'address': 'Admin Address', 'phone': '010-0000-0000', 'email': 'admin@example.com'}
}

def users_append(root):
    def append_user():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        confirm_password = reg_confirm_password_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        
        if username in users:
            messagebox.showerror("회원가입 오류", "이미 존재하는 아이디입니다")
        elif password != confirm_password:
            messagebox.showerror("비밀번호 오류", "비밀번호가 일치하지 않습니다")
        elif not username or not password or not address or not phone or not email:
            messagebox.showerror("회원가입 오류", "모든 필드를 채워주세요")
        else:
            users[username] = {'password': password, 'address': address, 'phone': phone, 'email': email}
            messagebox.showinfo("회원가입 완료", "회원가입이 완료되었습니다")
            register_window.destroy()

    register_window = Toplevel()
    register_window.title("회원가입")
    register_window.geometry("300x500")
    
    Label(register_window, text="아이디").pack(pady=5)
    reg_username_entry = Entry(register_window)
    reg_username_entry.pack(pady=5)
    
    Label(register_window, text="비밀번호").pack(pady=5)
    reg_password_entry = Entry(register_window, show="*")
    reg_password_entry.pack(pady=5)

    Label(register_window, text="비밀번호 확인").pack(pady=5)
    reg_confirm_password_entry = Entry(register_window, show="*")
    reg_confirm_password_entry.pack(pady=5)
    
    Label(register_window, text="주소").pack(pady=5)
    address_entry = Entry(register_window)
    address_entry.pack(pady=5)

    Label(register_window, text="전화번호").pack(pady=5)
    phone_entry = Entry(register_window)
    phone_entry.pack(pady=5)

    Label(register_window, text="이메일").pack(pady=5)
    email_entry = Entry(register_window)
    email_entry.pack(pady=5)
    
    Button(register_window, text="회원가입", command=append_user).pack(pady=10)

def users_info(root):
    user_info_window = Toplevel()
    user_info_window.title("사용자 정보")
    user_info_window.geometry("200x200")

    row = 0
    for username, info in users.items():
        Label(user_info_window, text=f"아이디: {username}").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text=f"주소: {info['address']}").grid(row=row+1, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text=f"전화번호: {info['phone']}").grid(row=row+2, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text=f"이메일: {info['email']}").grid(row=row+3, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text="").grid(row=row+4, column=0)  # 빈 줄 추가
        row += 5

def users_info_edit(root):
    def open_edit_window(username):
        def update_user_info():
            new_password = password_entry.get()
            new_address = address_entry.get()
            new_phone = phone_entry.get()
            new_email = email_entry.get()
            
            if not new_password or not new_address or not new_phone or not new_email:
                messagebox.showerror("입력오류", "모든 필드를 입력하세요")
                return

            users[username]['password'] = new_password
            users[username]['address'] = new_address
            users[username]['phone'] = new_phone
            users[username]['email'] = new_email

            messagebox.showinfo("수정 완료", "사용자 정보가 수정되었습니다")
            edit_window.destroy()
            user_info_window.destroy()
            users_info_edit()

        edit_window = Toplevel()    
        Label(edit_window, text="새 비밀번호").pack(pady=5)
        password_entry = Entry(edit_window, show="*")
        password_entry.insert(0, users[username]['password'])
        password_entry.pack(pady=5)

        Label(edit_window, text="새 주소").pack(pady=5)
        address_entry = Entry(edit_window)
        address_entry.insert(0, users[username]['address'])
        address_entry.pack(pady=5)

        Label(edit_window, text="새 전화번호").pack(pady=5)
        phone_entry = Entry(edit_window)
        phone_entry.insert(0, users[username]['phone'])
        phone_entry.pack(pady=5)

        Label(edit_window, text="새 이메일").pack(pady=5)
        email_entry = Entry(edit_window)
        email_entry.insert(0, users[username]['email'])
        email_entry.pack(pady=5)

        Button(edit_window, text="저장", command=update_user_info).pack(pady=10)

    user_info_window = Toplevel()
    user_info_window.title("사용자 정보")
    user_info_window.geometry("200x200")

    row = 0
    for username, info in users.items():
        Label(user_info_window, text=f"아이디: {username}").grid(row=row, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text=f"주소: {info['address']}").grid(row=row+1, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text=f"전화번호: {info['phone']}").grid(row=row+2, column=0, sticky='w', padx=10, pady=5)
        Label(user_info_window, text=f"이메일: {info['email']}").grid(row=row+3, column=0, sticky='w', padx=10, pady=5)
        Button(user_info_window, text="수정", command=lambda u=username: open_edit_window(u)).grid(row=row+4, column=0, pady=5)
        Label(user_info_window, text="").grid(row=row+5, column=0)  # 빈 줄 추가
        row += 6

def users_delete(root):
    def delete_user():
        username = username_entry.get()
        
        if username not in users:
            messagebox.showerror("삭제 오류", "존재하지 않는 아이디입니다")
        else:
            del users[username]
            messagebox.showinfo("삭제 완료", "사용자 정보가 삭제되었습니다")
            delete_window.destroy()

    delete_window = Toplevel()
    delete_window.title("사용자 삭제")
    delete_window.geometry("300x200")

    Label(delete_window, text="아이디").pack(pady=5)
    username_entry = Entry(delete_window)
    username_entry.pack(pady=5)
    
    Button(delete_window, text="삭제", command=delete_user).pack(pady=10)
