import tkinter as tk
from tkinter import messagebox

from data_base_connect import connection


class Client_Input(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.check_data_btn = btn
        self.check_data_btn.configure(text="Далее", command=self.check_data)

        # Создание кнопочек
        self.client_first_name_label = tk.Label(self, text="Имя:")
        self.client_first_name_entry = tk.Entry(self)

        self.client_second_name_label = tk.Label(self, text="Фамилия:")
        self.client_second_name_entry = tk.Entry(self)

        self.client_address_label = tk.Label(self, text="Адрес:")
        self.client_address_entry = tk.Entry(self)

        self.client_telephone_label = tk.Label(self, text="Телефон:")
        self.client_telephone_entry = tk.Entry(self)

        self.existing_user_btn = tk.Button(self, text="Выбрать существующего пользователя",
                                           command=self.select_existing_user)

        # Позиционирование
        self.client_first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.client_first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.client_second_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.client_second_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.client_address_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.client_address_entry.grid(row=2, column=1, padx=10, pady=5)

        self.client_telephone_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.client_telephone_entry.grid(row=3, column=1, padx=10, pady=5)

        self.existing_user_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def frame_pack(self):
        self.pack()

    def frame_close(self):
        self.pack_forget()

    # Сбор данных
    def collect_data(self):
        client_first_name = self.client_first_name_entry.get()
        client_second_name = self.client_second_name_entry.get()
        client_address = self.client_address_entry.get()
        client_telephone = self.client_telephone_entry.get()
        return client_first_name, client_second_name, client_address, client_telephone

    def select_existing_user(self):
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, second_name, address, telephone FROM client")
        clients = cursor.fetchall()
        cursor.close()

        if not clients:
            messagebox.showinfo("Info", "Нет существующих пользователей")
            return

        select_window = tk.Toplevel(self)
        select_window.title("Выберите пользователя")

        for client in clients:
            client_info = f"{client[1]} {client[2]}, Адрес: {client[3]}, Телефон: {client[4]}"
            btn = tk.Button(select_window, text=client_info,
                            command=lambda c=client: self.use_existing_user(c, select_window))
            btn.pack()

    def use_existing_user(self, client, window):
        self.client_first_name_entry.delete(0, tk.END)
        self.client_first_name_entry.insert(0, client[1])
        self.client_second_name_entry.delete(0, tk.END)
        self.client_second_name_entry.insert(0, client[2])
        self.client_address_entry.delete(0, tk.END)
        self.client_address_entry.insert(0, client[3])
        self.client_telephone_entry.delete(0, tk.END)
        self.client_telephone_entry.insert(0, client[4])
        window.destroy()

    def check_data(self):
        client_first_name, client_second_name, client_address, client_telephone = self.collect_data()

        if not client_first_name or not client_second_name or not client_address or not client_telephone:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        self.client_first_name_entry.delete(0, tk.END)
        self.client_second_name_entry.delete(0, tk.END)
        self.client_address_entry.delete(0, tk.END)
        self.client_telephone_entry.delete(0, tk.END)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM client WHERE first_name=%s AND second_name=%s AND address=%s AND telephone=%s",
                       (client_first_name, client_second_name, client_address, client_telephone))
        existing_client = cursor.fetchone()

        if existing_client:
            messagebox.showinfo("Успех", f"Использован существующий пользователь с ID: {existing_client[0]}")
            cursor.close()
            client_id = existing_client[0]
            self.parent.get_client_id(client_id)
            return

        cursor.execute(
            "INSERT INTO client (first_name, second_name, address, telephone, created_at) "
            "VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP) RETURNING id",
            (client_first_name, client_second_name, client_address, client_telephone))
        new_client_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        messagebox.showinfo("Успех", f"Новый пользователь успешно добавлен с ID: {new_client_id}")
        client_id = new_client_id[0]
        self.parent.get_client_id(client_id)
        return
