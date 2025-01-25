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
        self.task_input.bind("<FocusIn>", self.clear_placeholder) #clear
        self.task_input.bind("<FocusOut>", self.restore_placeholder) #out of focus

        # Adding tasks button
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        # Tasks display
        self.task_list = tk.Listbox(self, font=(
            "Futura", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter a task...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter a task...")
            self.task_input.configure(style="Custom.TEntry")


if __name__ == '__main__':
    app = TaskTracker()
    app.mainloop()