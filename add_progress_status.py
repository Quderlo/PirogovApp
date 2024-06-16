from tkinter import messagebox, ttk

from data_base_connect import connection
import tkinter as tk


class Add_Progress_Status(tk.Toplevel):
    def __init__(self, parent, order_id):
        super().__init__(parent)
        self.parent = parent
        self.order_id = order_id
        self.title("Добавить Прогресс")

        self.status_label = tk.Label(self, text="Статус:")
        self.status_label.pack(pady=5)
        self.status_combobox = ttk.Combobox(self, values=["Ожидает запчастей", "В процессе ремонта", "Готово к выдаче", "Завершено"])
        self.status_combobox.pack(pady=5)

        self.notes_label = tk.Label(self, text="Заметки:")
        self.notes_label.pack(pady=5)
        self.notes_text = tk.Text(self, height=10, width=40)
        self.notes_text.pack(pady=5)

        self.add_btn = tk.Button(self, text="Добавить", command=self.add_progress)
        self.add_btn.pack(pady=10)

    def add_progress(self):
        status = self.status_combobox.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not status or not notes:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        cursor = connection.cursor()

        cursor.execute("INSERT INTO progress (status, notes, id_order) VALUES (%s, %s, %s)",
                       (status, notes, self.order_id))
        connection.commit()
        cursor.close()

        messagebox.showinfo("Успех", "Прогресс успешно добавлен")
        self.destroy()
        self.parent.load_progress()