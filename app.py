import tkinter as tk
from frames.create_order import Create_Order_Frame
from frames.worker import Worker_Frame
from frames.client import Client_Frame
from frames.directory import Dictionary_Frame
from frames.order import Order_Frame
from frames.login import Login_Frame


class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Компастер")
        # self.attributes('-toolwindow', 1)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        # self.resizable(True, True)
        self.button_activation = True

        button_frame = tk.Frame(self)
        button_frame.pack(anchor=tk.N)

        self.login_btn = tk.Button(button_frame)
        self.login_btn.pack(side=tk.LEFT, pady=10)

        self.create_order_btn = tk.Button(button_frame)
        self.create_order_btn.pack(side=tk.LEFT, pady=10)

        self.order_btn = tk.Button(button_frame)
        self.order_btn.pack(side=tk.LEFT, pady=10)

        self.worker_btn = tk.Button(button_frame)
        self.worker_btn.pack(side=tk.LEFT, pady=10)

        self.client_btn = tk.Button(button_frame)
        self.client_btn.pack(side=tk.LEFT, pady=10)

        self.dictionary_btn = tk.Button(button_frame)
        self.dictionary_btn.pack(side=tk.LEFT, pady=10)

        self.create_order = Create_Order_Frame(self, self.create_order_btn)
        self.order = Order_Frame(self, self.order_btn)
        self.worker = Worker_Frame(self, self.worker_btn)
        self.client = Client_Frame(self, self.client_btn)
        self.dictionary = Dictionary_Frame(self, self.dictionary_btn)

        self.buttons_activation()

        self.login = Login_Frame(self, self.login_btn)

    def buttons_activation(self):
        if self.button_activation:
            self.create_order_btn.configure(state="disabled")
            self.order_btn.configure(state="disabled")
            self.worker_btn.configure(state="disabled")
            self.client_btn.configure(state="disabled")
            self.dictionary_btn.configure(state="disabled")
        else:
            self.create_order_btn.configure(state="normal")
            self.order_btn.configure(state="normal")
            self.worker_btn.configure(state="normal")
            self.client_btn.configure(state="normal")
            self.dictionary_btn.configure(state="normal")

        self.button_activation = not self.button_activation

