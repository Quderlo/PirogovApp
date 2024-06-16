import tkinter as tk
from tkinter import messagebox

from data_base_connect import connection


class Worker_Input(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.check_data_btn = btn
        self.check_data_btn.configure(text="Далее", command=self.check_data)

        # Создание кнопочег
        self.worker_first_name_label = tk.Label(self, text="Имя:")
        self.worker_first_name_entry = tk.Entry(self)

        self.worker_second_name_label = tk.Label(self, text="Фамилия:")
        self.worker_second_name_entry = tk.Entry(self)

        self.worker_telephone_label = tk.Label(self, text="Телефон:")
        self.worker_telephone_entry = tk.Entry(self)

        self.existing_data_btn = tk.Button(self, text="Выбрать существующего работника",
                                             command=self.select_existing_worker)

        # Позиционирование
        self.worker_first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.worker_first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.worker_second_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.worker_second_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.worker_telephone_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.worker_telephone_entry.grid(row=2, column=1, padx=10, pady=5)

        self.existing_data_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def frame_pack(self):
        self.pack()

    def frame_close(self):
        self.pack_forget()

    # Сбор данных
    def collect_data(self):
        worker_first_name = self.worker_first_name_entry.get()
        worker_second_name = self.worker_second_name_entry.get()
        worker_telephone = self.worker_telephone_entry.get()
        return worker_first_name, worker_second_name, worker_telephone

    def select_existing_worker(self):
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, second_name, telephone FROM worker")
        workers = cursor.fetchall()
        cursor.close()

        if not workers:
            messagebox.showinfo("Info", "Нет существующих работников")
            return

        select_window = tk.Toplevel(self)
        select_window.title("Выберите работника")

        for worker in workers:
            worker_info = f"{worker[1]} {worker[2]}, Телефон: {worker[3]}"
            btn = tk.Button(select_window, text=worker_info,
                            command=lambda w=worker: self.use_existing_data(w, select_window))
            btn.pack()

    def use_existing_data(self, worker, window):
        self.worker_first_name_entry.delete(0, tk.END)
        self.worker_first_name_entry.insert(0, worker[1])
        self.worker_second_name_entry.delete(0, tk.END)
        self.worker_second_name_entry.insert(0, worker[2])
        self.worker_telephone_entry.delete(0, tk.END)
        self.worker_telephone_entry.insert(0, worker[3])
        window.destroy()
        self.data_id = worker[0]

    def check_data(self):
        worker_first_name, worker_second_name, worker_telephone = self.collect_data()


        if not worker_first_name or not worker_second_name or not worker_telephone:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        self.worker_first_name_entry.delete(0, tk.END)
        self.worker_second_name_entry.delete(0, tk.END)
        self.worker_telephone_entry.delete(0, tk.END)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM worker WHERE first_name=%s AND second_name=%s AND telephone=%s",
                       (worker_first_name, worker_second_name, worker_telephone))
        existing_data = cursor.fetchone()

        if existing_data:
            messagebox.showinfo("Успех", f"Использован существующий работник с ID: {existing_data[0]}")
            cursor.close()
            data_id = existing_data[0]
            self.parent.get_worker_id(data_id)
            return

        cursor.execute(
            "INSERT INTO worker (first_name, second_name, telephone) "
            "VALUES (%s, %s, %s) RETURNING id",
            (worker_first_name, worker_second_name, worker_telephone))
        new_worker_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        messagebox.showinfo("Успех", f"Новый пользователь успешно добавлен с ID: {new_worker_id}")
        data_id = new_worker_id
        self.parent.get_worker_id(data_id)
        return
