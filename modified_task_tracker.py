import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json

class TaskTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Meliora Task Tracker")
        self.geometry("650x650")
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

        # Deadline
        self.deadline_label = ttk.Label(self, text = "Deadline (MM-DD-YYYY):").pack(pady=5) # deadline label
        self.deadline_input = ttk.Entry(self, font = "Futura")
        self.deadline_input.pack(pady=5)

        # Adding tasks button
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        # Own tabs for each category
        self.notebook = ttk.Notebook(self) # use ttk.Notebook
        self.notebook.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 10)
        
            # ttk.Frame
            # store work school personal in own frame
            # own list per category

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
        deadline = self.deadline_input.get()

        if task != "Enter a task...":
            all_data = f"{task} | {category} | {priority} | {deadline}"
            self.task_list.insert(tk.END, all_data)

            if priority == "Very Important!":
                self.task_list.itemconfig(tk.END, fg="red")
            else:
                self.task_list.itemconfig(tk.END, fg="green")

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

    def edit_task(self):
        task_index = self.task_list.curselection() # get what is clicked
        if task_index: 
            chosen_task = self.task_list.get(task_index)
            separate_data = chosen_task.split(" | ") # separate task name, category, priority
            
            # create a new window for edit
            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Task")

            # input box
            self.edit_name = ttk.Entry(edit_window, font=(
                "Futura", 12), width=30, style="Custon.TEntry")
            self.edit_name.insert(0, separate_data[0]) # input current chosen task
            self.edit_name.pack(padx=10, pady=10)

            # category
            self.edit_category = ttk.Combobox(edit_window, values = ["Work", "Personal", "School"])
            self.edit_category.set(separate_data[1])
            self.edit_category.pack(pady=5)

            # priority
            self.edit_priority = ttk.Combobox(edit_window, values = ["Very Important!", "Not so Important"])
            self.edit_priority.set(separate_data[2])
            self.edit_priority.pack(pady=5)

            # deadline
            self.edit_deadline = ttk.Entry(edit_window, font = "Futura")
            self.edit_deadline.insert(0, separate_data[3])
            self.edit_deadline.pack(pady=5)

            # save button
            ttk.Button(edit_window, text = "Save", command = lambda: self.save_changes(task_index, edit_window)).pack(pady=5) #lambda - inner function so that i can use the variables for an outside function

    def save_changes(self, task_index, edit_window):
        new_name = self.edit_name.get()
        new_category = self.edit_category.get()
        new_priority = self.edit_priority.get()
        new_deadline = self.edit_deadline.get()

        new_data = f"{new_name} | {new_category} | {new_priority} | {new_deadline}"
        self.task_list.delete(task_index)
        self.task_list.insert(task_index, new_data)

        if new_priority == "Very Important!":
            self.task_list.itemconfig(task_index, fg="red")
        else:
            self.task_list.itemconfig(task_index, fg="green")

        self.save_tasks() # called save_tasks function
        edit_window.destroy() # destroy window once saved
            
    def progress(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "gray":
                done_count += 1
        messagebox.showinfo("Task Progress", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def mark_done(self):
        task_index = self.task_list.curselection()
        current = self.task_list.get(task_index)

        if task_index:
            task_done = f"{current} | DONE"
            self.task_list.delete(task_index)
            self.task_list.insert(task_index, task_done)
            self.task_list.itemconfig(task_index, fg="gray")
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