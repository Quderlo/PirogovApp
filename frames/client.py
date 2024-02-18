import tkinter as tk
from tkinter import ttk
from data_base_connect import connection


class Client_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Клиенты", command=self.frame_pack)

        self.tree = ttk.Treeview(self, columns=("First Name", "Second Name", "Address", "Telephone", "Created At"),
                                 show="headings")
        self.tree.heading("First Name", text="Имя")
        self.tree.heading("Second Name", text="Фамилия")
        self.tree.heading("Address", text="Адрес")
        self.tree.heading("Telephone", text="Телефон")
        self.tree.heading("Created At", text="Дата создания")
        self.tree.pack(expand=True, fill="both")

    def frame_pack(self):
        self.pack()
        self.load_data()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Клиенты", command=self.frame_pack)

    def load_data(self):
        # Очищаем таблицу перед загрузкой новых данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем данные из базы данных
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, second_name, adress, telephone, created_at FROM client")
        clients = cursor.fetchall()

        # Заполняем таблицу данными
        for client in clients:
            self.tree.insert("", "end", values=client)
