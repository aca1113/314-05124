import tkinter as tk
from tkinter import colorchooser
import pickle
import os

class ObsidianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Obsidian - To-Do List")

        # Initialize them colors
        self.bg_color = "#2E0854"         # Purple background
        self.entry_color = "#4B0082"      # Darker purple
        self.button_color = "#800080"     # Purple button color
        self.listbox_color = "#4B0082"    # Darker purple for listbox
        self.text_color = "white"         # White text color

        self.tasks = []
        self.xp = 0
        self.level = 1
        self.load_data()

        # Create main canvas and scrollbar
        self.canvas = tk.Canvas(root, bg=self.bg_color)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.create_widgets()

    def create_widgets(self):
        # Search Entry
        self.search_label = tk.Label(self.scrollable_frame, text="Search Task:", bg=self.bg_color, fg=self.text_color)
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_entry = tk.Entry(self.scrollable_frame, width=40, font=("Helvetica", 12))
        self.search_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.search_entry.bind("<KeyRelease>", self.update_task_listbox)

        # Task Entry
        self.task_label = tk.Label(self.scrollable_frame, text="Task Name:", bg=self.bg_color, fg=self.text_color)
        self.task_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.task_entry = tk.Entry(self.scrollable_frame, width=40, font=("Helvetica", 12), bg=self.entry_color, fg=self.text_color)
        self.task_entry.grid(row=3, column=0, padx=10, pady=10)

        # Impact Dropdown
        self.impact_label = tk.Label(self.scrollable_frame, text="Impact Level:", bg=self.bg_color, fg=self.text_color)
        self.impact_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.impact_var = tk.StringVar(self.scrollable_frame)
        self.impact_var.set("Medium")  # Default value
        self.impact_menu = tk.OptionMenu(self.scrollable_frame, self.impact_var, "Low", "Medium", "High")
        self.impact_menu.config(bg=self.entry_color, fg=self.text_color)
        self.impact_menu.grid(row=5, column=0, padx=10, pady=10)

        # Add Task Button
        self.add_button = tk.Button(self.scrollable_frame, text="Add Task", command=self.add_task, bg=self.button_color, fg=self.text_color)
        self.add_button.grid(row=6, column=0, padx=10, pady=10)

        # Task Listbox with context menu
        self.task_listbox = tk.Listbox(self.scrollable_frame, width=50, height=10, font=("Helvetica", 12), bg=self.listbox_color, fg=self.text_color)
        self.task_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.task_listbox.bind("<Button-3>", self.show_context_menu)
        self.update_task_listbox()

        # XP Label
        self.xp_label = tk.Label(self.scrollable_frame, text=f"Level: {self.level} | XP: {self.xp}/30", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        self.xp_label.grid(row=8, column=0, padx=10, pady=10)

        # XP Bar
        self.xp_bar = tk.Canvas(self.scrollable_frame, width=200, height=20, bg=self.listbox_color)
        self.xp_bar.grid(row=8, column=1, padx=10, pady=10)
        self.update_xp_bar()

        # Complete Task Button
        self.complete_button = tk.Button(self.scrollable_frame, text="Complete Task", command=self.complete_task, bg=self.button_color, fg=self.text_color)
        self.complete_button.grid(row=9, column=0, padx=10, pady=10)

        # Delete Task Button
        self.delete_button = tk.Button(self.scrollable_frame, text="Delete Task", command=self.delete_task, bg=self.button_color, fg=self.text_color)
        self.delete_button.grid(row=9, column=1, padx=10, pady=10)

        # Settings Button
        self.settings_button = tk.Button(self.scrollable_frame, text="Settings", command=self.open_settings, bg=self.button_color, fg=self.text_color)
        self.settings_button.grid(row=10, column=0, padx=10, pady=10)

        # Analytics Button
        self.analytics_button = tk.Button(self.scrollable_frame, text="View Analytics", command=self.show_analytics, bg=self.button_color, fg=self.text_color)
        self.analytics_button.grid(row=10, column=1, padx=10, pady=10)

        # Subtask Entry and Button
        self.subtask_label = tk.Label(self.scrollable_frame, text="Subtask Name:", bg=self.bg_color, fg=self.text_color)
        self.subtask_label.grid(row=11, column=0, padx=10, pady=10, sticky="w")
        self.subtask_entry = tk.Entry(self.scrollable_frame, width=40, font=("Helvetica", 12), bg=self.entry_color, fg=self.text_color)
        self.subtask_entry.grid(row=12, column=0, padx=10, pady=10)
        self.subtask_button = tk.Button(self.scrollable_frame, text="Add Subtask", command=self.add_subtask, bg=self.button_color, fg=self.text_color)
        self.subtask_button.grid(row=12, column=1, padx=10, pady=10)

        # Task Editing Entry and Button
        self.edit_task_label = tk.Label(self.scrollable_frame, text="Edit Task Name:", bg=self.bg_color, fg=self.text_color)
        self.edit_task_label.grid(row=13, column=0, padx=10, pady=10, sticky="w")
        self.edit_task_entry = tk.Entry(self.scrollable_frame, width=40, font=("Helvetica", 12), bg=self.entry_color, fg=self.text_color)
        self.edit_task_entry.grid(row=14, column=0, padx=10, pady=10)
        self.edit_button = tk.Button(self.scrollable_frame, text="Edit Task", command=self.edit_task, bg=self.button_color, fg=self.text_color)
        self.edit_button.grid(row=14, column=1, padx=10, pady=10)

        # Task Sort Button
        self.sort_button = tk.Button(self.scrollable_frame, text="Sort by Impact", command=self.sort_tasks, bg=self.button_color, fg=self.text_color)
        self.sort_button.grid(row=15, column=0, padx=10, pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        impact = self.impact_var.get()
        if task:
            self.tasks.append({"task": task, "impact": impact, "subtasks": [], "completed": False})
            self.task_entry.delete(0, tk.END)
            self.update_task_listbox()
            self.save_data()

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]['completed'] = True
            self.xp += 10
            if self.xp >= 30:
                self.xp -= 30
                self.level += 1
            self.update_task_listbox()
            self.update_xp_bar()
            self.save_data()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.update_task_listbox()
            self.save_data()

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            self.edit_task_entry.delete(0, tk.END)
            self.edit_task_entry.insert(0, task['task'])
            self.edit_task_entry.bind("<FocusOut>", lambda e: self.save_task_edit(selected_task_index[0]))

    def save_task_edit(self, index):
        new_task = self.edit_task_entry.get().strip()
        if new_task:
            impact = self.impact_var.get()
            self.tasks[index].update({"task": new_task, "impact": impact})
            self.update_task_listbox()
            self.save_data()

    def add_subtask(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            subtask = self.subtask_entry.get().strip()
            if subtask:
                self.tasks[selected_task_index[0]]['subtasks'].append(subtask)
                self.subtask_entry.delete(0, tk.END)
                self.update_task_listbox()
                self.save_data()

    def update_task_listbox(self, event=None):
        self.task_listbox.delete(0, tk.END)
        search_term = self.search_entry.get().lower()
        for task in self.tasks:
            if search_term in task['task'].lower():
                display_text = f"{task['task']} (Impact: {task.get('impact', 'None')})"
                if task.get('completed'):
                    display_text = "[COMPLETED] " + display_text
                self.task_listbox.insert(tk.END, display_text)

    def update_xp_bar(self):
        self.xp_label.config(text=f"Level: {self.level} | XP: {self.xp}/30")
        self.xp_bar.delete("all")
        fill_percentage = self.xp / 30 * 200
        self.xp_bar.create_rectangle(0, 0, fill_percentage, 20, fill="#00FF00")

    def sort_tasks(self):
        impact_levels = {"Low": 1, "Medium": 2, "High": 3}
        self.tasks.sort(key=lambda x: impact_levels.get(x['impact'], 0))
        self.update_task_listbox()

    def save_data(self):
        with open("obsidian_data.dat", "wb") as file:
            data = {"tasks": self.tasks, "xp": self.xp, "level": self.level}
            pickle.dump(data, file)

    def load_data(self):
        if os.path.exists("obsidian_data.dat"):
            with open("obsidian_data.dat", "rb") as file:
                data = pickle.load(file)
                self.tasks = data.get("tasks", [])
                self.xp = data.get("xp", 0)
                self.level = data.get("level", 1)

    def open_settings(self):
        # Update colors via color chooser
        self.bg_color = colorchooser.askcolor(title="Choose Background Color")[1] or self.bg_color
        self.entry_color = colorchooser.askcolor(title="Choose Entry Color")[1] or self.entry_color
        self.button_color = colorchooser.askcolor(title="Choose Button Color")[1] or self.button_color
        self.listbox_color = colorchooser.askcolor(title="Choose Listbox Color")[1] or self.listbox_color
        self.text_color = colorchooser.askcolor(title="Choose Text Color")[1] or self.text_color
        self.update_widgets_colors()

    def update_widgets_colors(self):
        self.root.configure(bg=self.bg_color)
        self.task_entry.configure(bg=self.entry_color, fg=self.text_color)
        self.add_button.configure(bg=self.button_color, fg=self.text_color)
        self.complete_button.configure(bg=self.button_color, fg=self.text_color)
        self.delete_button.configure(bg=self.button_color, fg=self.text_color)
        self.settings_button.configure(bg=self.button_color, fg=self.text_color)
        self.analytics_button.configure(bg=self.button_color, fg=self.text_color)
        self.subtask_button.configure(bg=self.button_color, fg=self.text_color)
        self.edit_button.configure(bg=self.button_color, fg=self.text_color)
        self.sort_button.configure(bg=self.button_color, fg=self.text_color)
        self.task_listbox.configure(bg=self.listbox_color, fg=self.text_color)
        self.xp_bar.configure(bg=self.listbox_color)

    def show_context_menu(self, event):
        if not hasattr(self, 'context_menu'):
            self.context_menu = tk.Menu(self.root, tearoff=0)
            self.context_menu.add_command(label="Complete", command=self.complete_task)
            self.context_menu.add_command(label="Delete", command=self.delete_task)
            self.context_menu.add_command(label="Add Subtask", command=self.add_subtask)
            self.context_menu.add_command(label="Edit Task", command=self.edit_task)
        self.context_menu.post(event.x_root, event.y_root)

    def show_analytics(self):
        # Directly update the UI with analytics info
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.get('completed')])
        analytics_text = (
            f"Total Tasks: {total_tasks}\n"
            f"Completed Tasks: {completed_tasks}\n"
            f"Tasks Remaining: {total_tasks - completed_tasks}\n"
            f"Current XP: {self.xp}\n"
            f"Current Level: {self.level}"
        )

        if hasattr(self, 'analytics_label'):
            self.analytics_label.destroy()
        self.analytics_label = tk.Label(self.scrollable_frame, text=analytics_text, bg=self.bg_color, fg=self.text_color)
        self.analytics_label.grid(row=16, column=0, columnspan=2, padx=10, pady=10)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ObsidianApp(root)
    root.mainloop()
