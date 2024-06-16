import tkinter as tk
from tkinter import ttk
from data_base_connect import connection


class Order_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Заказы", command=self.frame_pack)

        self.tree = ttk.Treeview(self, columns=("Description", "Total Cost", "Serial Number", "Created At", "Worker", "Directory"), show="headings")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Total Cost", text="Общая стоимость")
        self.tree.heading("Serial Number", text="Серийный номер")
        self.tree.heading("Created At", text="Дата создания")
        self.tree.heading("Worker", text="Работник")
        self.tree.heading("Directory", text="Техника")
        self.tree.pack(expand=True, fill="both")

    def frame_pack(self):
        self.pack()
        self.load_data()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Заказы", command=self.frame_pack)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = connection.cursor()
        cursor.execute("SELECT o.description, o.total_cost, o.serial_number, o.created_at, w.first_name || ' ' || w.second_name AS worker_name, d.name AS directory_name "
                       "FROM \"order\" o "
                       "JOIN worker w ON o.worker_id = w.id "
                       "JOIN directory d ON o.directory_id = d.id")
        orders = cursor.fetchall()

        # Заполняем таблицу данными
        for order in orders:
            self.tree.insert("", "end", values=order)