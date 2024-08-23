import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pickle
import os

class catalog:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory catalog")
        self.root.geometry("700x550")
        self.root.config(bg="#2C3E50")

        # Default file path
        self.default_file_path = "inventory.dat"

        self.items = []

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(root, bg="#2C3E50")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the UI components
        self.frame = tk.Frame(self.canvas, bg="#2C3E50")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.title_label = tk.Label(self.frame, text="Inventory Manager", font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="#ECF0F1")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        self.name_label = tk.Label(self.frame, text="Item Name:", font=("Helvetica", 12), bg="#2C3E50", fg="#ECF0F1")
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(self.frame, font=("Helvetica", 12), width=25)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.desc_label = tk.Label(self.frame, text="Description:", font=("Helvetica", 12), bg="#2C3E50", fg="#ECF0F1")
        self.desc_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.desc_entry = tk.Entry(self.frame, font=("Helvetica", 12), width=25)
        self.desc_entry.grid(row=2, column=1, padx=10, pady=10)

        self.category_label = tk.Label(self.frame, text="Category:", font=("Helvetica", 12), bg="#2C3E50", fg="#ECF0F1")
        self.category_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.category_entry = tk.Entry(self.frame, font=("Helvetica", 12), width=25)
        self.category_entry.grid(row=3, column=1, padx=10, pady=10)

        self.upload_button = tk.Button(self.frame, text="Upload Image", command=self.upload_image, font=("Helvetica", 12), bg="#3498DB", fg="#ECF0F1", activebackground="#2980B9")
        self.upload_button.grid(row=4, column=0, padx=10, pady=10)
        self.image_label = tk.Label(self.frame, text="No image", font=("Helvetica", 12), bg="#2C3E50", fg="#ECF0F1")
        self.image_label.grid(row=4, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.frame, text="Add Item", command=self.add_item, font=("Helvetica", 12), bg="#27AE60", fg="#ECF0F1", activebackground="#229954")
        self.add_button.grid(row=5, column=0, padx=10, pady=10)

        self.edit_button = tk.Button(self.frame, text="Edit Item", command=self.edit_item, font=("Helvetica", 12), bg="#F39C12", fg="#ECF0F1", activebackground="#D68910")
        self.edit_button.grid(row=5, column=1, padx=10, pady=10)

        self.remove_button = tk.Button(self.frame, text="Remove Item", command=self.remove_item, font=("Helvetica", 12), bg="#E74C3C", fg="#ECF0F1", activebackground="#C0392B")
        self.remove_button.grid(row=6, column=0, padx=10, pady=10)

        self.listbox = tk.Listbox(self.frame, width=50, font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1", selectbackground="#2980B9")
        self.listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.load_button = tk.Button(self.frame, text="Load Item", command=self.load_item, font=("Helvetica", 12), bg="#9B59B6", fg="#ECF0F1", activebackground="#8E44AD")
        self.load_button.grid(row=8, column=0, padx=10, pady=10)

        self.save_button = tk.Button(self.frame, text="Save Inventory", command=self.save_inventory, font=("Helvetica", 12), bg="#1ABC9C", fg="#ECF0F1", activebackground="#16A085")
        self.save_button.grid(row=8, column=1, padx=10, pady=10)

        self.load_inventory_button = tk.Button(self.frame, text="Load Inventory", command=self.load_inventory, font=("Helvetica", 12), bg="#2980B9", fg="#ECF0F1", activebackground="#2471A3")
        self.load_inventory_button.grid(row=9, column=0, padx=10, pady=10, columnspan=2)

        self.image_path = None

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.image_path = file_path
            img = Image.open(self.image_path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img, text="")
            self.image_label.image = img

    def add_item(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        category = self.category_entry.get()

        if not name:
            messagebox.showerror("Error", "Item name is required.")
            return

        item = {"name": name, "desc": desc, "category": category, "image": self.image_path}
        self.items.append(item)
        self.listbox.insert(tk.END, f"{name} ({category})")
        self.clear_entries()

    def edit_item(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected.")
            return

        name = self.name_entry.get()
        desc = self.desc_entry.get()
        category = self.category_entry.get()

        if not name:
            messagebox.showerror("Error", "Item name is required.")
            return

        item = {"name": name, "desc": desc, "category": category, "image": self.image_path}
        self.items[selected_index[0]] = item
        self.listbox.delete(selected_index)
        self.listbox.insert(selected_index, f"{name} ({category})")
        self.clear_entries()

    def remove_item(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected.")
            return

        self.listbox.delete(selected_index)
        del self.items[selected_index[0]]
        self.clear_entries()

    def load_item(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected.")
            return

        item = self.items[selected_index[0]]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item["name"])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, item["desc"])
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, item["category"])

        if item["image"]:
            img = Image.open(item["image"])
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img, text="")
            self.image_label.image = img
        else:
            self.image_label.config(image="", text="No image")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.image_label.config(image="", text="No image")
        self.category_entry.delete(0, tk.END)
        self.image_path = None

    def save_inventory(self):
        with open(self.default_file_path, 'wb') as file:
            pickle.dump(self.items, file)
        messagebox.showinfo("Success", "Inventory saved successfully.")

    def load_inventory(self):
        if os.path.exists(self.default_file_path):
            with open(self.default_file_path, 'rb') as file:
                self.items = pickle.load(file)
            self.listbox.delete(0, tk.END)
            for item in self.items:
                self.listbox.insert(tk.END, f"{item['name']} ({item['category']})")
            messagebox.showinfo("Success", "Inventory loaded successfully.")
        else:
            messagebox.showerror("Error", "No inventory file found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = catalog(root)
    root.mainloop()
