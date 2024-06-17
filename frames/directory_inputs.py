import tkinter as tk
from tkinter import messagebox

from data_base_connect import connection


class Directory_Input(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.check_data_btn = btn
        self.check_data_btn.configure(text="Далее", command=self.check_data)

        # Создание кнопочек
        self.directory_name_label = tk.Label(self, text="Название:")
        self.directory_name_entry = tk.Entry(self)

        self.directory_type_label = tk.Label(self, text="Тип:")
        self.directory_type_entry = tk.Entry(self)

        self.existing_directory_btn = tk.Button(self, text="Выбрать существующего технику",
                                                command=self.select_existing_directory)

        # Позиционирование
        self.directory_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.directory_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.directory_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.directory_type_entry.grid(row=1, column=1, padx=10, pady=5)

        self.existing_directory_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def frame_pack(self):
        self.pack()

    def frame_close(self):
        self.pack_forget()

    # Сбор данных
    def collect_data(self):
        directory_name = self.directory_name_entry.get()
        directory_type = self.directory_type_entry.get()
        return directory_name, directory_type

    def select_existing_directory(self):
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, type FROM directory")
        directories = cursor.fetchall()
        cursor.close()

        if not directories:
            messagebox.showinfo("Info", "Нет существующей техники")
            return

        select_window = tk.Toplevel(self)
        select_window.title("Выберите пользователя")

        for directory in directories:
            directory_info = f"Название: {directory[1]}, Тип: {directory[2]}"
            btn = tk.Button(select_window, text=directory_info,
                            command=lambda c=directory: self.use_existing_directory(c, select_window))
            btn.pack()

    def use_existing_directory(self, client, window):
        self.directory_name_entry.delete(0, tk.END)
        self.directory_name_entry.insert(0, client[1])
        self.directory_type_entry.delete(0, tk.END)
        self.directory_type_entry.insert(0, client[2])
        window.destroy()

    def check_data(self):
        directory_name, directory_type = self.collect_data()

        if not directory_name or not directory_type:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        self.directory_name_entry.delete(0, tk.END)
        self.directory_type_entry.delete(0, tk.END)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM directory WHERE name=%s AND type=%s",
                       (directory_name, directory_type))
        existing_directory = cursor.fetchone()

        if existing_directory:
            messagebox.showinfo("Успех", f"Использована существующая техника с ID: {existing_directory[0]}")
            cursor.close()
            directory_id = existing_directory[0]
            self.parent.get_directory_id(directory_id)
            return

        cursor.execute(
            "INSERT INTO directory (name, type) "
            "VALUES (%s, %s) RETURNING id",
            (directory_name, directory_type))
        new_directory_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        messagebox.showinfo("Успех", f"Новая техника успешно добавлена с ID: {new_directory_id}")
        directory_id = new_directory_id
        self.parent.get_directory_id(directory_id)
        return
