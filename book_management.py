import tkinter as tk
from tkinter import Toplevel, Entry, Label, Button, Scrollbar, messagebox, Menu
from tkinter import ttk
from models import Book
from user_management import users_append, users_info, users_info_edit, users_delete
import csv

books = []
rented_books = []

def show_main_window(root):
    global tree
    root.title("도서 관리 프로그램")
    root.geometry("1200x800")

    # 책 목록을 표시할 Treeview 위젯
    columns = ('카테고리', 'ISBN', '제목', '장르 번호', '저자', '출판사', '가격')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=0, column=0, sticky='nsew')

    # Scrollbar 추가
    sb = Scrollbar(root, command=tree.yview)
    tree.config(yscrollcommand=sb.set)
    sb.grid(row=0, column=1, sticky='ns')

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # 메뉴 설정
    mb = Menu(root)

    fi = Menu(mb, tearoff=0)  # 도서정보관리
    fi.add_command(label="도서 검색", command=lambda: book_search(root))
    fi.add_command(label="도서 추가", command=lambda: book_append(root))
    fi.add_command(label="도서 수정", command=lambda: book_correction(root))
    fi.add_command(label="도서 삭제", command=lambda: book_delete(root))
    fi.add_separator()
    mb.add_cascade(label="도서 관리", menu=fi)  # 도서관리

    u = Menu(mb, tearoff=0)
    u.add_command(label="회원 추가", command=lambda: users_append(root))
    u.add_command(label="회원 정보", command=lambda: users_info(root))
    u.add_command(label="회원 정보 수정", command=lambda: users_info_edit(root))
    u.add_command(label="회원 삭제", command=lambda: users_delete(root))
    u.add_separator()
    mb.add_cascade(label="회원정보", menu=u)  # 회원정보 관리

    b = Menu(mb, tearoff=0)
    b.add_command(label="대여 신청", command=lambda: book_rental())
    b.add_command(label="대여 현황", command=lambda: show_rented_books(root))
    # b.add_command(label="대여 정보", command=lambda: book_rental(root))
    b.add_separator()
    mb.add_cascade(label="대여", menu=b)  # 대여정보관리

    root.config(menu=mb)

def refresh_book_list(filtered_books=None):
    for row in tree.get_children():
        tree.delete(row)
    book_list = books if filtered_books is None else filtered_books
    for book in book_list:
        tree.insert('', 'end', values=book.to_tuple())

# 도서 추가 기능 구현
def book_append(root):
    def add_book():
        category = category_entry.get()
        isbn = isbn_entry.get()
        title = title_entry.get()
        gn = gn_entry.get()
        author = author_entry.get()
        publisher = publisher_entry.get()
        price = price_entry.get()

        if category and isbn and title and gn and author and publisher and price:
            new_book = Book(category, isbn, title, gn, author, publisher, price)
            books.append(new_book)
            refresh_book_list()
            save_book_to_file()
            add_book_window.destroy()
        else:
            messagebox.showwarning("입력오류", "모든 필드를 입력하세요.")

    add_book_window = Toplevel(root)
    add_book_window.title("도서 추가")
    add_book_window.geometry("300x500")

    Label(add_book_window, text="카테고리").pack(pady=5)
    category_entry = Entry(add_book_window)
    category_entry.pack(pady=5)

    Label(add_book_window, text="ISBN").pack(pady=5)
    isbn_entry = Entry(add_book_window)
    isbn_entry.pack(pady=5)

    Label(add_book_window, text="책 제목").pack(pady=5)
    title_entry = Entry(add_book_window)
    title_entry.pack(pady=5)

    Label(add_book_window, text="장르 번호").pack(pady=5)
    gn_entry = Entry(add_book_window)
    gn_entry.pack(pady=5)

    Label(add_book_window, text="저자").pack(pady=5)
    author_entry = Entry(add_book_window)
    author_entry.pack(pady=5)

    Label(add_book_window, text="출판사").pack(pady=5)
    publisher_entry = Entry(add_book_window)
    publisher_entry.pack(pady=5)

    Label(add_book_window, text="가격").pack(pady=5)
    price_entry = Entry(add_book_window)
    price_entry.pack(pady=5)

    Button(add_book_window, text="추가", command=add_book).pack(pady=10)

def book_search(root):
    def search():
        keyword = keyword_entry.get().lower()
        filtered_books = [book for book in books if keyword in book.isbn.lower() or
                                                    keyword in book.title.lower() or 
                                                    keyword in book.author.lower() or 
                                                    keyword in book.publisher.lower()]
        refresh_book_list(filtered_books)
        search_window.destroy()

    search_window = Toplevel(root)
    search_window.title("도서 검색")
    search_window.geometry("300x200")
        
    Label(search_window, text="검색키워드").pack(pady=5)
    keyword_entry = Entry(search_window)
    keyword_entry.pack(pady=5)

    Button(search_window, text="검색", command=search).pack(pady=10)

def book_correction(root):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("경고","수정할 도서를 선택하세요.")
        return

    selected_book = tree.item(selected_item)["values"]
    selected_index = tree.index(selected_item)
    def update_book():
        category = category_entry.get()
        isbn = isbn_entry.get()
        title = title_entry.get()
        gn = gn_entry.get()
        author = author_entry.get()
        publisher = publisher_entry.get()
        price = price_entry.get()

        if category and isbn and title and gn and author and publisher and price:
            updated_book = Book(category, isbn, title, gn, author, publisher, price)
            books[selected_index] = updated_book
            refresh_book_list()
            save_book_to_file()
            edit_book_window.destroy()
        else:
            messagebox.showerror("입력오류", "모든필드를 입력하세요")
    
    edit_book_window = Toplevel(root)
    edit_book_window.title("도서 수정")
    edit_book_window.geometry("300x500")

    Label(edit_book_window, text="카테고리").pack(pady=5)
    category_entry = Entry(edit_book_window)
    category_entry.insert(0, selected_book[0])
    category_entry.pack(pady=5)

    Label(edit_book_window, text="ISBN").pack(pady=5)
    isbn_entry = Entry(edit_book_window)
    isbn_entry.insert(0, selected_book[1])
    isbn_entry.pack(pady=5)

    Label(edit_book_window, text="책 제목").pack(pady=5)
    title_entry = Entry(edit_book_window)
    title_entry.insert(0, selected_book[2])
    title_entry.pack(pady=5)

    Label(edit_book_window, text="장르 번호").pack(pady=5)
    gn_entry = Entry(edit_book_window)
    gn_entry.insert(0, selected_book[3])
    gn_entry.pack(pady=5)

    Label(edit_book_window, text="저자").pack(pady=5)
    author_entry = Entry(edit_book_window)
    author_entry.insert(0, selected_book[4])
    author_entry.pack(pady=5)

    Label(edit_book_window, text="출판사").pack(pady=5)
    publisher_entry = Entry(edit_book_window)
    publisher_entry.insert(0, selected_book[5])
    publisher_entry.pack(pady=5)

    Label(edit_book_window, text="가격").pack(pady=5)
    price_entry = Entry(edit_book_window)
    price_entry.insert(0, selected_book[6])
    price_entry.pack(pady=5)

    Button(edit_book_window, text="수정", command=update_book).pack(pady=10)

def book_delete(root):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("경고", "삭제할 도서를 선택하세요")
        return
    selected_index = tree.index(selected_item)
    del books[selected_index]
    save_book_to_file()
    refresh_book_list()

def save_book_to_file():
    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for book in books:
            writer.writerow(book.to_tuple())

def load_books_from_file():
    try:
        with open('books.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                book = Book.from_tuple(row)
                books.append(book)
    except FileNotFoundError:
        pass

def book_rental():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("경고", "대여할 도서를 선택하세요")
        return
    
    selected_book = tree.item(selected_item)["values"]

    rented_books.append(selected_book)
    messagebox.showinfo("대여완료", f"'{selected_book[2]}'도서가 대여되었습니다.")

def show_rented_books(root):
    rented_books_window = Toplevel(root)
    rented_books_window.title("대여된 도서 목록")
    rented_books_window.geometry("500x400")

    columns = ('카테고리', 'ISBN', '제목', '장르 번호', '저자', '출판사', '가격')
    rented_tree = ttk.Treeview(rented_books_window, columns=columns, show='headings')
    for col in columns:
        rented_tree.heading(col, text=col)
    rented_tree.pack(fill='both', expand=True)

    for book in rented_books:
        rented_tree.insert('', 'end', values=book)