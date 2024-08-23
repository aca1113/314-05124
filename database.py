import os
import re
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, scrolledtext
import base64

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Engine")
        self.root.geometry("1100x600")

        self.dat_folder = os.path.join(os.getcwd(), 'databases')
        if not os.path.exists(self.dat_folder):
            os.makedirs(self.dat_folder)

        # Sidebar and Treeview Frame
        self.left_frame = tk.Frame(root, width=200, bg="#003366")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Sidebar
        self.sidebar = tk.Frame(self.left_frame, bg="#004080", width=150)
        self.sidebar.pack(side=tk.TOP, fill=tk.Y)

        # Buttons
        self.new_button = ttk.Button(self.sidebar, text="New File", command=self.new_file)
        self.new_button.pack(fill=tk.X, padx=5, pady=5)

        self.open_button = ttk.Button(self.sidebar, text="Open File", command=self.open_file)
        self.open_button.pack(fill=tk.X, padx=5, pady=5)

        self.save_button = ttk.Button(self.sidebar, text="Save File", command=self.save_file)
        self.save_button.pack(fill=tk.X, padx=5, pady=5)

        self.search_button = ttk.Button(self.sidebar, text="Search", command=self.search)
        self.search_button.pack(fill=tk.X, padx=5, pady=5)

        self.replace_button = ttk.Button(self.sidebar, text="Replace", command=self.replace)
        self.replace_button.pack(fill=tk.X, padx=5, pady=5)

        self.regex_button = ttk.Button(self.sidebar, text="Regex", command=self.regex_search_replace)
        self.regex_button.pack(fill=tk.X, padx=5, pady=5)

        # Treeview
        self.tree = ttk.Treeview(self.left_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.load_file)

        # Editor Frame
        self.editor_frame = tk.Frame(root, bg="#003366")
        self.editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Line Counter
        self.line_counter_frame = tk.Frame(self.editor_frame, bg="#003366")
        self.line_counter_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.line_counter = tk.Text(self.line_counter_frame, width=4, padx=3, takefocus=0, border=0,
                                    background='#004080', state='disabled', wrap='none')
        self.line_counter.pack(side=tk.LEFT, fill=tk.Y)

        # Text Editor
        self.editor = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, bg="#002147",
                                                fg="#FFFFFF", insertbackground="white", undo=True)
        self.editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.editor.bind('<KeyRelease>', self.update_line_counter)

        # Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#003366", foreground="white", rowheight=25, fieldbackground="#003366")
        style.map("Treeview", background=[('selected', '#004080')])

        self.colors = ["#FF5733", "#FFBD33", "#DBFF33", "#75FF33", "#33FF57", "#33FFBD", "#33DBFF", "#3375FF"]
        self.color_index = 0

        self.load_tree()
        self.update_line_counter()

    def encode_text_to_binary(self, text):
        text_bytes = text.encode('utf-8')
        encoded_text = base64.b64encode(text_bytes).decode('utf-8')
        return encoded_text

    def decode_binary_to_text(self, binary_data):
        decoded_bytes = base64.b64decode(binary_data.encode('utf-8'))
        return decoded_bytes.decode('utf-8')

    def load_tree(self):
        self.tree.delete(*self.tree.get_children())
        for root_dir, dirs, files in os.walk(self.dat_folder):
            for dir_name in dirs:
                dir_id = self.tree.insert('', 'end', text=dir_name, open=True)
                self.load_files(dir_id, os.path.join(root_dir, dir_name))
            for file_name in files:
                if file_name.endswith('.dat'):
                    self.tree.insert('', 'end', text=file_name)

    def load_files(self, parent, dir_path):
        for file_name in os.listdir(dir_path):
            if file_name.endswith('.dat'):
                self.tree.insert(parent, 'end', text=file_name)

    def load_file(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        file_name = self.tree.item(selected_item, "text")
        file_path = os.path.join(self.dat_folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                encoded_content = file.read().decode('utf-8')
                content = self.decode_binary_to_text(encoded_content)
                self.editor.delete(1.0, tk.END)
                self.editor.insert(tk.END, content)
                self.color_text()

    def save_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        file_name = self.tree.item(selected_item, "text")
        file_path = os.path.join(self.dat_folder, file_name)

        content = self.editor.get(1.0, tk.END).strip()
        encoded_content = self.encode_text_to_binary(content)

        with open(file_path, 'wb') as file:
            file.write(encoded_content.encode('utf-8'))

    def new_file(self):
        file_name = simpledialog.askstring("New File", "Enter new file name (with .dat extension):")
        if file_name and not file_name.endswith('.dat'):
            file_name += '.dat'
        if file_name:
            file_path = os.path.join(self.dat_folder, file_name)
            with open(file_path, 'wb') as file:
                file.write(b"")  # Create an empty binary file
            self.load_tree()

    def open_file(self):
        file_name = filedialog.askopenfilename(initialdir=self.dat_folder, title="Open File",
                                              filetypes=(("Data files", "*.dat"), ("All files", "*.*")))
        if file_name:
            self.load_existing_file(os.path.basename(file_name))

    def load_existing_file(self, file_name):
        file_path = os.path.join(self.dat_folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                encoded_content = file.read().decode('utf-8')
                content = self.decode_binary_to_text(encoded_content)
                self.editor.delete(1.0, tk.END)
                self.editor.insert(tk.END, content)
                self.color_text()

    def update_line_counter(self, event=None):
        self.line_counter.config(state='normal')
        self.line_counter.delete(1.0, tk.END)

        current_line = self.editor.index(tk.END).split('.')[0]
        line_numbers = "\n".join(str(i) for i in range(1, int(current_line)))
        self.line_counter.insert(tk.END, line_numbers)
        self.line_counter.config(state='disabled')

    def search(self):
        search_term = simpledialog.askstring("Search", "Enter text to search:")
        if search_term:
            start = '1.0'
            while True:
                start = self.editor.search(search_term, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.editor.tag_add('search', start, end)
                self.editor.tag_config('search', background='yellow')
                start = end

    def replace(self):
        search_term = simpledialog.askstring("Search", "Enter text to search:")
        replace_term = simpledialog.askstring("Replace", "Enter replacement text:")
        if search_term is not None and replace_term is not None:
            start = '1.0'
            while True:
                start = self.editor.search(search_term, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.editor.delete(start, end)
                self.editor.insert(start, replace_term)
                start = f"{start}+{len(replace_term)}c"

    def regex_search_replace(self):
        search_pattern = simpledialog.askstring("Regex Search", "Enter regex pattern:")
        replace_term = simpledialog.askstring("Replace", "Enter replacement text:")
        if search_pattern and replace_term is not None:
            text = self.editor.get(1.0, tk.END)
            new_text = re.sub(search_pattern, replace_term, text)
            self.editor.delete(1.0, tk.END)
            self.editor.insert(tk.END, new_text)
            self.color_text()

    def color_text(self):
        self.editor.tag_configure("colored", foreground=self.colors[self.color_index])
        text = self.editor.get(1.0, tk.END)
        self.editor.delete(1.0, tk.END)
        self.color_index = (self.color_index + 1) % len(self.colors)
        for i, char in enumerate(text):
            color_tag = f"colored_{i % len(self.colors)}"
            self.editor.tag_config(color_tag, foreground=self.colors[i % len(self.colors)])
            self.editor.insert(tk.END, char, color_tag)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
