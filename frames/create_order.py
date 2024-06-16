import tkinter as tk
from frames.client_inputs import Client_Input
from frames.directory_inputs import Directory_Input
from frames.worker_inputs import Worker_Input
from frames.order_inputs import Order_Input


class Create_Order_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Оформить заказ", command=self.frame_pack)

        self.check_data_btn = tk.Button(self, text="Далее")
        self.check_data_btn.pack()
        self.client_inputs = Client_Input(self, self.check_data_btn)
        self.client_inputs = Client_Input(self, self.check_data_btn)

        self.directory_inputs = None
        self.worker_inputs = None
        self.order_inputs = None

        # Данные
        self.client_id = None
        self.directory_id = None
        self.worker_id = None

    def frame_pack(self):
        self.pack()
        self.client_inputs.frame_pack()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Оформить заказ", command=self.frame_pack)

    def get_client_id(self, data_id):
        self.client_id = data_id
        self.client_inputs.frame_close()
        self.directory_inputs = Directory_Input(self, self.check_data_btn)
        self.directory_inputs.frame_pack()

    def get_directory_id(self, data_id):
        self.directory_id = data_id
        self.directory_inputs.frame_close()
        self.worker_inputs = Worker_Input(self, self.check_data_btn)
        self.worker_inputs.frame_pack()

    def get_worker_id(self, data_id):
        self.worker_id = data_id
        self.worker_inputs.frame_close()
        self.order_inputs = Order_Input(self, self.check_data_btn)
        self.order_inputs.frame_pack()

    def finish_order(self):
        self.order_inputs.frame_close()
        self.frame_close()
