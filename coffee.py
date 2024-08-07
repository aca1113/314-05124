# coffee.py
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, colorchooser
import os
import keyword

class coffee(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Currently opened file path
        self.current_file = None
        
        # Set up the layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Side panel for file explorer
        self.file_explorer_frame = ttk.Frame(self, width=200)
        self.file_explorer_frame.grid(row=0, column=0, sticky="ns")
        
        self.file_listbox = tk.Listbox(self.file_explorer_frame)
        self.file_listbox.pack(fill='both', expand=True)
        self.file_listbox.bind('<<ListboxSelect>>', self.open_selected_file)
        
        self.load_folder_button = ttk.Button(self.file_explorer_frame, text="Open Folder", command=self.load_folder)
        self.load_folder_button.pack(pady=5)
        
        # Main editor area with a line counter
        self.editor_frame = ttk.Frame(self)
        self.editor_frame.grid(row=0, column=1, sticky="nsew")
        
        self.line_numbers = tk.Text(self.editor_frame, width=4, padx=4, takefocus=0, border=0, background='lightgrey', state='disabled')
        self.line_numbers.pack(side='left', fill='y')
        
        self.text_area = tk.Text(self.editor_frame, undo=True, wrap='none')
        self.text_area.pack(expand=True, fill='both')
        self.text_area.bind('<KeyRelease>', self.on_key_release)
        
        # Save button
        self.save_button = ttk.Button(self.editor_frame, text="Save", command=self.save_file)
        self.save_button.pack(pady=5)
        
        # Find and Replace
        self.find_button = ttk.Button(self.editor_frame, text="Find/Replace", command=self.open_find_replace_dialog)
        self.find_button.pack(pady=5)
        
        # Theme customization
        self.theme_button = ttk.Button(self.editor_frame, text="Change Theme", command=self.change_theme)
        self.theme_button.pack(pady=5)
        
        # Set up tags for syntax highlighting
        self.text_area.tag_configure("keyword", foreground="blue")
        self.text_area.tag_configure("comment", foreground="green")
        self.text_area.tag_configure("string", foreground="orange")
        
        # Set default theme colors
        self.default_bg = self.text_area.cget("background")
        self.default_fg = self.text_area.cget("foreground")
        
    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.file_listbox.delete(0, tk.END)
            for file_name in os.listdir(folder_path):
                if file_name.endswith(('.py', '.txt', '.html', '.js')):  # Supported file types
                    self.file_listbox.insert(tk.END, os.path.join(folder_path, file_name))

    def open_selected_file(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            file_path = self.file_listbox.get(selected_index)
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path
            self.update_line_numbers()
            self.highlight_syntax()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("HTML files", "*.html"), ("JavaScript files", "*.js"), ("All files", "*.*")])
        if file_path:
            self.current_file = file_path
            self.save_file()

    def update_line_numbers(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        
        line_count = self.text_area.index(tk.END).split('.')[0]
        line_numbers_string = "\n".join(str(i) for i in range(1, int(line_count)))
        
        self.line_numbers.insert(tk.END, line_numbers_string)
        self.line_numbers.config(state='disabled')

    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.highlight_syntax()

    def highlight_syntax(self):
        content = self.text_area.get(1.0, tk.END)
        
        # Clear existing tags
        self.text_area.tag_remove("keyword", 1.0, tk.END)
        self.text_area.tag_remove("comment", 1.0, tk.END)
        self.text_area.tag_remove("string", 1.0, tk.END)

        # Highlight keywords
        for word in keyword.kwlist:
            start_index = 1.0
            while True:
                start_index = self.text_area.search(r'\b' + word + r'\b', start_index, stopindex=tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                self.text_area.tag_add("keyword", start_index, end_index)
                start_index = end_index
        
        # Highlight comments (for Python, JavaScript)
        comment_patterns = [r'#.*', r'//.*']
        for pattern in comment_patterns:
            start_index = 1.0
            while True:
                start_index = self.text_area.search(pattern, start_index, stopindex=tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index} lineend"
                self.text_area.tag_add("comment", start_index, end_index)
                start_index = end_index

        # Highlight strings (single and double quotes)
        string_patterns = [r'".*?"', r"'.*?'"]
        for pattern in string_patterns:
            start_index = 1.0
            while True:
                start_index = self.text_area.search(pattern, start_index, stopindex=tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(self.text_area.get(start_index, start_index + ' lineend'))}c"
                self.text_area.tag_add("string", start_index, end_index)
                start_index = end_index

    def open_find_replace_dialog(self):
        self.find_replace_window = tk.Toplevel(self)
        self.find_replace_window.title("Find and Replace")
        
        tk.Label(self.find_replace_window, text="Find:").grid(row=0, column=0, sticky="e")
        self.find_entry = tk.Entry(self.find_replace_window)
        self.find_entry.grid(row=0, column=1, padx=2, pady=2, sticky="we")
        
        tk.Label(self.find_replace_window, text="Replace:").grid(row=1, column=0, sticky="e")
        self.replace_entry = tk.Entry(self.find_replace_window)
        self.replace_entry.grid(row=1, column=1, padx=2, pady=2, sticky="we")
        
        self.find_button = ttk.Button(self.find_replace_window, text="Find", command=self.find_text)
        self.find_button.grid(row=0, column=2, padx=2, pady=2)
        
        self.replace_button = ttk.Button(self.find_replace_window, text="Replace", command=self.replace_text)
        self.replace_button.grid(row=1, column=2, padx=2, pady=2)
        
        self.find_replace_window.grid_columnconfigure(1, weight=1)

    def find_text(self):
        self.text_area.tag_remove('found', '1.0', tk.END)
        find_text = self.find_entry.get()
        if find_text:
            start_index = '1.0'
            while True:
                start_index = self.text_area.search(find_text, start_index, stopindex=tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(find_text)}c"
                self.text_area.tag_add('found', start_index, end_index)
                start_index = end_index
            self.text_area.tag_config('found', background='yellow')

    def replace_text(self):
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()
        if find_text and replace_text:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_text, replace_text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)
            self.highlight_syntax()
            
    def change_theme(self):
        color = colorchooser.askcolor(title="Choose background color")[1]
        if color:
            self.text_area.config(bg=color)
            self.line_numbers.config(bg=color)
