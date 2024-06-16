import tkinter as tk
from tkinter import messagebox
from data_base_connect import connection


class Order_Input(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.check_data_btn = btn
        self.check_data_btn.configure(text="Создать заказ", command=self.add_order)

        # Создание полей ввода и кнопок
        self.description_label = tk.Label(self, text="Описание:")
        self.description_entry = tk.Entry(self)

        self.total_cost_label = tk.Label(self, text="Общая стоимость:")
        self.total_cost_entry = tk.Entry(self)

        self.serial_number_label = tk.Label(self, text="Серийный номер:")
        self.serial_number_entry = tk.Entry(self)

        # Позиционирование с использованием grid
        self.description_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.description_entry.grid(row=0, column=1, padx=10, pady=5)

        self.total_cost_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.total_cost_entry.grid(row=1, column=1, padx=10, pady=5)

        self.serial_number_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.serial_number_entry.grid(row=2, column=1, padx=10, pady=5)

    def frame_pack(self):
        self.pack()

    def frame_close(self):
        self.pack_forget()

    # Сбор данных
    def collect_data(self):
        description = self.description_entry.get()
        total_cost = self.total_cost_entry.get()
        serial_number = self.serial_number_entry.get()
        directory_id = self.parent.directory_id
        client_id = self.parent.client_id
        worker_id = self.parent.worker_id
        return description, total_cost, serial_number, directory_id, client_id, worker_id

    def add_order(self):
        description, total_cost, serial_number, directory_id, client_id, worker_id = self.collect_data()

        if not description or not total_cost or not serial_number:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        cursor = connection.cursor()

        # Выполнение SQL-запроса для добавления заказа
        cursor.execute(
            "INSERT INTO \"order\" (description, total_cost, serial_number, created_at, directory_id, client_id, worker_id) "
            "VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s) RETURNING id",
            (description, total_cost, serial_number, directory_id, client_id, worker_id))

        new_order_id = cursor.fetchone()[0]
        connection.commit()

        cursor.execute("INSERT INTO progress (status, notes, created_at, id_order) VALUES "
                       "(%s, %s, CURRENT_TIMESTAMP, %s)",
                       ("Передано в приёмке", "Ожидание принятия в работу", new_order_id))
        connection.commit()

        cursor.close()

        messagebox.showinfo("Успех", f"Новый заказ успешно добавлен с ID: {new_order_id}")

        self.description_entry.delete(0, tk.END)
        self.total_cost_entry.delete(0, tk.END)
        self.serial_number_entry.delete(0, tk.END)

        self.parent.finish_order()
        return

