import tkinter as tk


class Client_Input(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Создание кнопочек
        self.client_first_name_label = tk.Label(self, text="Имя:")
        self.client_first_name_entry = tk.Entry(self)

        self.client_second_name_label = tk.Label(self, text="Фамилия:")
        self.client_second_name_entry = tk.Entry(self)

        self.client_address_label = tk.Label(self, text="Адрес:")
        self.client_address_entry = tk.Entry(self)

        self.client_telephone_label = tk.Label(self, text="Телефон:")
        self.client_telephone_entry = tk.Entry(self)

        # Позиционирование
        self.client_first_name_label.pack(side=tk.LEFT, pady=25)
        self.client_first_name_entry.pack(side=tk.LEFT, pady=25)

        self.client_second_name_label.pack(side=tk.LEFT, pady=25)
        self.client_second_name_entry.pack(side=tk.LEFT, pady=25)

        self.client_address_label.pack(side=tk.LEFT, pady=25)
        self.client_address_entry.pack(side=tk.LEFT, pady=25)

        self.client_telephone_label.pack(side=tk.LEFT, pady=25)
        self.client_telephone_entry.pack(side=tk.LEFT, pady=25)

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
