import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os

class launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("MAIN DECK")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")

        self.slots = [None] * 21
        self.selected_slot = None
        self.text_file = "slots.txt"

        # Load previous slot assignments
        self.load_slots()

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="MAIN DECK", font=("Arial", 24), fg="white", bg="black")
        title_label.pack(pady=20)

        # Slot Buttons
        self.buttons_frame = tk.Frame(self.root, bg="black")
        self.buttons_frame.pack(pady=10)

        self.slot_buttons = []
        for i in range(21):
            btn = tk.Button(self.buttons_frame, text=f"Slot {i+1}", command=lambda i=i: self.select_slot(i), bg="#2c2c2c", fg="white", font=("Arial", 12))
            btn.grid(row=i//7, column=i%7, padx=10, pady=10)
            self.slot_buttons.append(btn)

        # Assign and Launch Buttons
        self.assign_button = tk.Button(self.root, text="Assign Executable", command=self.assign_executable, bg="#1e90ff", fg="white", font=("Arial", 16))
        self.assign_button.pack(pady=10)

        self.launch_button = tk.Button(self.root, text="Launch", command=self.launch_executable, bg="#ff4500", fg="white", font=("Arial", 16))
        self.launch_button.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(self.root, text="No slot selected", font=("Arial", 14), fg="white", bg="black")
        self.status_label.pack(pady=10)

        # Gradient Animation
        self.animate()

    def select_slot(self, index):
        self.selected_slot = index
        self.status_label.config(text=f"Selected Slot: {index+1}")
        self.status_label.config(fg="lightblue")

    def assign_executable(self):
        if self.selected_slot is None:
            messagebox.showwarning("Warning", "No slot selected")
            return
        
        file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if file_path:
            self.slots[self.selected_slot] = file_path
            self.save_slots()  # Save the updated slot assignments
            messagebox.showinfo("Info", f"Executable assigned to Slot {self.selected_slot + 1}")

    def launch_executable(self):
        if self.selected_slot is None:
            messagebox.showwarning("Warning", "No slot selected")
            return
        
        executable = self.slots[self.selected_slot]
        if executable:
            try:
                subprocess.run([executable], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to launch executable: {e}")
            except FileNotFoundError:
                messagebox.showerror("Error", "Executable file not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No executable assigned to selected slot")

    def save_slots(self):
        with open(self.text_file, 'w') as f:
            for slot in self.slots:
                if slot is not None:
                    f.write(f"{slot}\n")
                else:
                    f.write("None\n")

    def load_slots(self):
        if os.path.exists(self.text_file):
            with open(self.text_file, 'r') as f:
                lines = f.readlines()
                self.slots = [line.strip() if line.strip() != "None" else None for line in lines]

    def animate(self):
        # Gradient Animation: Change background color
        current_color = self.root.cget("bg")
        new_color = "#00008b" if current_color == "#1e90ff" else "#1e90ff"
        self.root.configure(bg=new_color)
        self.status_label.config(bg=new_color)
        self.root.after(1000, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = launcher(root)
    root.mainloop()
