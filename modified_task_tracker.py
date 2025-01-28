import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style, Progressbar
import json

class TaskTracker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Meliora Task Tracker")
        self.geometry("700x700")
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

        # store work school personal in own frame
        self.tabs = {} # array to create own tab
        self.task_lists = {} # array to create own list

        for category in ["Work", "Personal", "School"]: # loop for each category to be stored in a tab
            tab = ttk.Frame(self.notebook) # ttk.Frame
            self.notebook.add(tab, text = category) # append a category to notebook
            self.tabs[category] = tab # creates a ttk.Frame for all categories

            # own list per category
            task_list = tk.Listbox(tab, font=(
                "Futura", 16), height=10, selectmode=tk.NONE) # tk.Listbox variable assigned to a specific tab
            task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.task_lists[category] = task_list # call array then assign to listbox

        # Edit Button
        ttk.Button(self, text="Edit", style="info.TButton", command=self.edit_task).pack(side=tk.LEFT, padx=10, pady=10)

        # buttons for done, delete, and progress
        ttk.Button(self, text="Mark done", style="success.TButton",
                  command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton",
                  command=self.delete_task).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="View Progress", style="info.TButton",
                  command=self.progress).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self, orient = "horizontal", mode = "determinate", length = 400)
        self.progress_bar.pack(side = tk.BOTTOM, padx = 10, pady = 10)
        
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
            all_data = f"{task} | {priority} | {deadline}"
            self.task_lists[category].insert(tk.END, all_data)

            if priority == "Very Important!":
                self.task_lists[category].itemconfig(tk.END, fg="red")
            else:
                self.task_lists[category].itemconfig(tk.END, fg="green")

            self.task_input.delete(0, tk.END)
            self.save_tasks()

    def save_tasks(self):
        data = {} # changed to dict for diff categories
        for category, task_list in self.task_lists.items(): # looping thru categories and its list in tasks_lists 
            data[category] = []
            for i in range(task_list.size()):
                text = task_list.get(i)
                color = task_list.itemcget(i, "fg")
                data[category].append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    def edit_task(self):
        current_tab = self.notebook.tab(self.notebook.select(), "text") # what is current tab | selects tab and gets its text
        task_index = self.task_lists[current_tab].curselection() # get what is clicked
        if task_index: 
            chosen_task = self.task_lists[current_tab].get(task_index)
            separate_data = chosen_task.split(" | ") # separate task name, category, priority
            
            # create a new window for edit
            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Task")
    
            # input box
            self.edit_name = ttk.Entry(edit_window, font=(
                "Futura", 12), width=30, style="Custon.TEntry")
            self.edit_name.insert(0, separate_data[0]) # input current chosen task
            self.edit_name.pack(padx=10, pady=10)
    
            # priority
            self.edit_priority = ttk.Combobox(edit_window, values = ["Very Important!", "Not so Important"])
            self.edit_priority.set(separate_data[1])
            self.edit_priority.pack(pady=5)
    
            # deadline
            self.edit_deadline = ttk.Entry(edit_window, font = "Futura")
            self.edit_deadline.insert(0, separate_data[2])
            self.edit_deadline.pack(pady=5)
    
            # save button
            ttk.Button(edit_window, text = "Save", command = lambda: self.save_changes(task_index, edit_window, current_tab)).pack(pady=5) #lambda - inner function so that i can use the variables for an outside function

    def save_changes(self, task_index, edit_window, current_tab):
        new_name = self.edit_name.get()
        new_priority = self.edit_priority.get()
        new_deadline = self.edit_deadline.get()
    
        new_data = f"{new_name} | {new_priority} | {new_deadline}"
        self.task_lists[current_tab].delete(task_index)
        self.task_lists[current_tab].insert(task_index, new_data)
    
        if new_priority == "Very Important!":
            self.task_lists[current_tab].itemconfig(task_index, fg="red")
        else:
            self.task_lists[current_tab].itemconfig(task_index, fg="green")
    
        self.save_tasks() # called save_tasks function
        edit_window.destroy() # destroy window once saved
            
    def progress(self):
        # get each tabs' count
        done_count = 0
        total_count = 0 # zero default
        # loop through all tabs then add
        for task_list in self.task_lists.values():
            total_count += task_list.size()
            for i in range(task_list.size()): # changed parameter to current task list size
                if task_list.itemcget(i, "fg") == "gray":
                    done_count += 1
        messagebox.showinfo("Task Progress", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def progress_bar_ud(self):
        # got from progress function, just to count
        done_count = 0
        total_count = 0
        for task_list in self.task_lists.values():
            total_count += task_list.size()
            for i in range(task_list.size()):
                if task_list.itemcget(i, "fg") == "gray":
                    done_count += 1

        if total_count > 0:
            self.progress_bar["value"] = (done_count / total_count) * 100
        else:
            self.progress_bar["value"] = 0

    def mark_done(self):
        current_tab = self.notebook.tab(self.notebook.select(), "text") # what is current tab
        task_index = self.task_lists[current_tab].curselection()
        current = self.task_lists[current_tab].get(task_index)
        
        if "Very Important!" in current:
            priority = "red"
        else:
            priority = "green"

        if self.task_lists[current_tab].itemcget(task_index, "fg") == "gray":
            undo = current.replace(" | DONE", "")
            self.task_lists[current_tab].delete(task_index)
            self.task_lists[current_tab].insert(task_index, undo)
            self.task_lists[current_tab].itemconfig(task_index, fg=priority)
        else: 
            task_done = f"{current} | DONE"
            self.task_lists[current_tab].delete(task_index)
            self.task_lists[current_tab].insert(task_index, task_done)
            self.task_lists[current_tab].itemconfig(task_index, fg="gray")

        self.progress_bar_ud()
        self.save_tasks()
    
    def delete_task(self):
        current_tab = self.notebook.tab(self.notebook.select(), "text") # what is current tab
        task_index = self.task_lists[current_tab].curselection()
        if task_index:
            self.task_lists[current_tab].delete(task_index)
            self.save_tasks()

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for category, tasks in data.items():
                    for task in tasks:
                        self.task_lists[category].insert(tk.END, task["text"])
                        self.task_lists[category].itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = TaskTracker()
    app.mainloop()