import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from data_base_connect import connection


class Create_Order_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Оформить заказ", command=self.frame_pack)

        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.description_label = tk.Label(self.input_new_frame, text="Описание:")
        self.description_entry = tk.Entry(self.input_new_frame)

        self.cost_label = tk.Label(self.input_new_frame, text="Примерная стоимость:")
        self.cost_entry = tk.Entry(self.input_new_frame)

        self.worker_first_name_label = tk.Label(self.input_new_frame, text="Имя:")
        self.worker_first_name_entry = tk.Entry(self.input_new_frame)

        self.worker_second_name_label = tk.Label(self.input_new_frame, text="Фамилия:")
        self.worker_second_name_entry = tk.Entry(self.input_new_frame)

        self.client_first_name_label = tk.Label(self.input_new_frame, text="Имя:")
        self.client_first_name_entry = tk.Entry(self.input_new_frame)

        self.client_second_name_label = tk.Label(self.input_new_frame, text="Фамилия:")
        self.client_second_name_entry = tk.Entry(self.input_new_frame)

        self.directory_name_label = tk.Label(self.input_new_frame, text="Название:")
        self.directory_name_entry = tk.Entry(self.input_new_frame)

        self.directory_type_label = tk.Label(self.input_new_frame, text="Тип:")
        self.directory_type_entry = tk.Entry(self.input_new_frame)

        self.add_data_btn = tk.Button(self.input_new_frame, text="Добавить", command=self.add_data)

        # Позиционирование
        self.description_label.pack(side=tk.LEFT, pady=25)
        self.description_entry.pack(side=tk.LEFT, pady=25)

        self.cost_label.pack(side=tk.LEFT, pady=25)
        self.cost_entry.pack(side=tk.LEFT, pady=25)

        self.worker_first_name_label.pack(side=tk.LEFT, pady=25)
        self.worker_first_name_entry.pack(side=tk.LEFT, pady=25)

        self.worker_second_name_label.pack(side=tk.LEFT, pady=25)
        self.worker_second_name_entry.pack(side=tk.LEFT, pady=25)

        self.description_label.pack(side=tk.LEFT, pady=25)
        self.description_entry.pack(side=tk.LEFT, pady=25)

        self.client_first_name_label.pack(side=tk.LEFT, pady=25)
        self.client_first_name_entry.pack(side=tk.LEFT, pady=25)

        self.client_second_name_label.pack(side=tk.LEFT, pady=25)
        self.client_second_name_entry.pack(side=tk.LEFT, pady=25)

        self.directory_name_label.pack(side=tk.LEFT, pady=25)
        self.directory_name_entry.pack(side=tk.LEFT, pady=25)

        self.directory_type_label.pack(side=tk.LEFT, pady=25)
        self.directory_type_entry.pack(side=tk.LEFT, pady=25)

        self.add_data_btn.pack(side=tk.LEFT, pady=25)

    def frame_pack(self):
        self.pack()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Оформить заказ", command=self.frame_pack)

    def add_data(self):
        number = self.description_entry.get()
        sector = self.cost_entry.get()

        if not (number and sector):
            mb.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM auditory WHERE Number = %s AND Sector = %s", (number, sector))
            count = cursor.fetchone()[0]
            if count > 0:
                mb.showerror("Ошибка", "Аудитория с таким номером и сектором уже существует")
                return
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при проверке уникальности: {str(e)}")
            return

        # Добавление в базу
        try:
            cursor.execute("INSERT INTO auditory (Number, Sector) VALUES (%s, %s)", (number, sector))
            connection.commit()
            mb.showinfo("Успех", "Данные успешно добавлены в базу")
            self.load_data()
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при добавлении данных в базу: {str(e)}")
