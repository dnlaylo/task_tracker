import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json

class TaskTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Meliora Task Tracker")
        self.geometry("400x400")
        style = Style(theme="darkly")
        style.configure("Custon.TEntry", foreground="gray")

if __name__ == '__main__':
    app = TaskTracker()
    app.mainloop()