import tkinter as tk
from tkinter import messagebox, ttk
import psutil

class taskforce:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x400")

        # Create and place widgets
        self.create_widgets()
        self.update_process_list()

    def create_widgets(self):
        # Create a Treeview to display processes
        self.tree = ttk.Treeview(self.root, columns=("PID", "Name", "Memory", "CPU"), show='headings')
        self.tree.heading("PID", text="PID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Memory", text="Memory (MB)")
        self.tree.heading("CPU", text="CPU (%)")
        self.tree.column("PID", width=80, anchor="center")
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Memory", width=100, anchor="e")
        self.tree.column("CPU", width=100, anchor="e")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a button to kill processes
        self.kill_button = tk.Button(self.root, text="Kill Process", command=self.kill_process)
        self.kill_button.pack(pady=5)

    def update_process_list(self):
        self.tree.delete(*self.tree.get_children())
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                self.tree.insert("", tk.END, values=(
                    proc.info['pid'],
                    proc.info['name'],
                    f"{proc.info['memory_info'].rss / (1024 * 1024):.2f}",
                    proc.info['cpu_percent']
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.root.after(5000, self.update_process_list)

    def kill_process(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a process to kill.")
            return

        item = self.tree.item(selected_item)
        pid = item['values'][0]

        try:
            process = psutil.Process(pid)
            process.kill()  # Use kill() as a more forceful method
            messagebox.showinfo("Success", f"Process {pid} terminated.")
        except psutil.NoSuchProcess:
            messagebox.showwarning("Error", f"Process {pid} does not exist.")
        except psutil.AccessDenied:
            messagebox.showwarning("Error", f"Access denied to terminate process {pid}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate process {pid}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = taskforce(root)
    root.mainloop()
