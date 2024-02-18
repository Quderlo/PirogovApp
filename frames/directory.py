import tkinter as tk
from tkinter import ttk
from data_base_connect import connection


class Dictionary_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Справочник", command=self.frame_pack)

        self.tree = ttk.Treeview(self, columns=("Name", "Type"), show="headings")
        self.tree.heading("Name", text="Название")
        self.tree.heading("Type", text="Тип")
        self.tree.pack(expand=True, fill="both")

    def frame_pack(self):
        self.pack()
        self.load_data()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Справочник", command=self.frame_pack)

    def load_data(self):
        # Очищаем таблицу перед загрузкой новых данных
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем данные из базы данных
        cursor = connection.cursor()
        cursor.execute("SELECT name, type FROM directory")
        directories = cursor.fetchall()

        # Заполняем таблицу данными
        for item in directories:
            self.tree.insert("", "end", values=item)
