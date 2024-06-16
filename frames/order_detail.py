import tkinter as tk
from tkinter import messagebox, ttk

from add_progress_status import Add_Progress_Status
from data_base_connect import connection


class Order_Detail_Window(tk.Frame):
    def __init__(self, parent, order_id):
        super().__init__(parent)
        self.parent = parent
        self.order_id = order_id

        self.detail_frame = tk.Frame(self)
        self.detail_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create Treeview to display order progress
        self.tree = ttk.Treeview(self.detail_frame, columns=("Status", "Notes"), show="headings")
        self.tree.heading("Status", text="Статус")
        self.tree.heading("Notes", text="Заметки")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Button to add new progress status
        self.add_progress_btn = tk.Button(self, text="Добавить Прогресс", command=self.open_add_progress_window)
        self.add_progress_btn.pack(pady=10)

        # Execute the query and display data
        self.load_progress()

    def load_progress(self):
        cursor = connection.cursor()

        # Clear existing entries in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Use '%s' as the placeholder for psycopg2
        cursor.execute("SELECT status, notes FROM progress WHERE id_order = %s", (self.order_id,))

        progress_details = cursor.fetchall()

        if progress_details:
            for progress in progress_details:
                status, notes = progress
                self.tree.insert("", "end", values=(status, notes))
        else:
            messagebox.showinfo("Info", f"Прогресс для заказа с id {self.order_id} не найден")

        cursor.close()

    def open_add_progress_window(self):
        Add_Progress_Status(self, self.order_id)
