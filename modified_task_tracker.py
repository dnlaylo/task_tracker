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

        # Input box
        self.task_input = ttk.Entry(self, font=(
            "Futura", 16), width=30, style="Custon.TEntry")
        self.task_input.pack(pady=10)

        # Placeholder for input field
        self.task_input.insert(0, "Enter a task...")

if __name__ == '__main__':
    app = TaskTracker()
    app.mainloop()