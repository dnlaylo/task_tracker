import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json

class TaskTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Meliora Task Tracker")
        self.geometry("600x600")
        self.style = Style(theme = "darkly")
        self.style.configure("Custon.TEntry", foreground="gray")

        # Light mode / Dark mode
        self.is_dark = True
        ttk.Button(self, text = "Dark/Light", command = self.change_theme).pack(pady=5)

        # Input box
        self.task_input = ttk.Entry(self, font=(
            "Futura", 16), width=30, style="Custon.TEntry")
        self.task_input.pack(pady=10)

        # Placeholder for input field
        self.task_input.insert(0, "Enter a task...")
        self.task_input.bind("<FocusIn>", self.clear_placeholder) #clear
        self.task_input.bind("<FocusOut>", self.restore_placeholder) #out of focus

        # Category
        self.category_label = ttk.Label(self, text = "Category:").pack(pady=5) # dropdown label
        self.category_values = ttk.Combobox(self, values = ["Work", "Personal", "School"]) # values
        self.category_values.set("Work")
        self.category_values.pack(pady=5)

        # Priority
        self.priority_label = ttk.Label(self, text = "Priority:").pack(pady=5) # dropdown label
        self.priority_values = ttk.Combobox(self, values = ["Very Important!", "Not so Important"]) # values
        self.priority_values.set("Very Important!")
        self.priority_values.pack(pady=5)

        # Adding tasks button
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        # Tasks display
        self.task_list = tk.Listbox(self, font=(
            "Futura", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Edit Button
        ttk.Button(self, text="Edit", style="info.TButton", command=self.edit_task).pack(side=tk.LEFT, padx=10, pady=10)

        # buttons for done, delete, and progress
        ttk.Button(self, text="Mark done", style="success.TButton",
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="View Progress", style="info.TButton",
                   command=self.progress).pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.load_tasks()

    def change_theme(self):
        # to toggle themes
        if self.is_dark:  
            self.style.theme_use("flatly")
        else:
            self.style.theme_use("darkly") 
        self.is_dark = not self.is_dark # change to either true/false

    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter a task...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter a task...")
            self.task_input.configure(style="Custom.TEntry")

    def add_task(self):
        task = self.task_input.get()
        category = self.category_values.get()
        priority = self.priority_values.get()

        if task != "Enter a task...":
            all_data = f"{task} | {category} | {priority}"
            self.task_list.insert(tk.END, all_data)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_tasks()

    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    #def edit_task(self):
        # get what is clicked
        # separate task name, category, priority
        # create a new window for edit
            # input box
            # category
            # priority
            # save button
            
    def progress(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1
        messagebox.showinfo("Task Progress", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.save_tasks()
    
    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = TaskTracker()
    app.mainloop()