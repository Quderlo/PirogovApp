import tkinter as tk
from frames.worker import Worker_Frame
from frames.client import Client_Frame
from frames.directory import Dictionary_Frame


class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Компастер")
        # self.attributes('-toolwindow', 1)
        self.geometry("1000x600")
        # self.resizable(True, True)
        self.button_activation = True

        button_frame = tk.Frame(self)
        button_frame.pack(anchor=tk.N)

        self.worker_btn = tk.Button(button_frame)
        self.worker_btn.pack(side=tk.LEFT, pady=10)
        self.client_btn = tk.Button(button_frame)
        self.client_btn.pack(side=tk.LEFT, pady=10)
        self.dictionary_btn = tk.Button(button_frame)
        self.dictionary_btn.pack(side=tk.LEFT, pady=10)

        self.worker = Worker_Frame(self, self.worker_btn)
        self.client = Client_Frame(self, self.client_btn)
        self.dictionary = Dictionary_Frame(self, self.dictionary_btn)

    def buttons_activation(self):
        if self.button_activation:
            self.worker_btn.configure(state="disabled")
            self.client_btn.configure(state="disabled")
            self.dictionary_btn.configure(state="disabled")
        else:
            self.worker_btn.configure(state="normal")
            self.client_btn.configure(state="normal")
            self.dictionary_btn.configure(state="normal")

        self.button_activation = not self.button_activation

