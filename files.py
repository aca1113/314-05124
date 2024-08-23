import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pathlib
import shutil
import time

class fexp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(sticky="nsew")
        
        # Configure the grid for the parent window to expand
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        
        # Configure the grid for this frame to expand
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.currentPath = tk.StringVar(value=str(pathlib.Path.cwd()))
        self.newFileName = tk.StringVar(value="File.txt")
        self.searchQuery = tk.StringVar()
        self.clipboard = None

        self.create_widgets()
        self.pathChange()

    def create_widgets(self):
        # Style Configuration
        style = ttk.Style()
        style.configure('TFrame', background='#000000')
        style.configure('TButton', background='#000000', foreground='#00FFFF', font=('Exo', 10, 'bold'))
        style.configure('TLabel', background='#000000', foreground='#00FFFF', font=('Exo', 10))
        style.configure('TEntry', background='#000000', foreground='#00FFFF', font=('Exo', 10))  # Black background
        style.configure('TListbox', background='#000000', foreground='#00FFFF', font=('Exo', 10))
        style.configure('TScrollbar', background='#000000', foreground='#00FFFF')

        # Folder Up Button
        ttk.Button(self, text='Folder Up', command=self.goBack).grid(sticky='nsew', column=0, row=0)

        # Current Path Entry (Editable)
        path_entry = ttk.Entry(self, textvariable=self.currentPath)
        path_entry.grid(sticky='nsew', column=1, row=0, ipady=10, ipadx=10)

        # Search Directory Button
        search_dir_button = ttk.Button(self, text='Search Directory', command=self.searchDirectory)
        search_dir_button.grid(sticky='nsew', column=2, row=0)

        # Create New File/Folder Button
        create_button = ttk.Button(self, text='Create', command=self.openCreatePopup)
        create_button.grid(sticky='nsew', column=0, row=1)

        # Search Bar and Button for Files
        search_entry = ttk.Entry(self, textvariable=self.searchQuery)
        search_entry.grid(sticky='nsew', column=1, row=1, ipady=10, ipadx=10)  # Increased height to match Folder Up button
        search_files_button = ttk.Button(self, text='Search Files', command=self.searchFiles)
        search_files_button.grid(sticky='nsew', column=2, row=1)

        # File Listbox
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=('Exo', 10), background='#000000', foreground='#00FFFF')
        self.listbox.grid(sticky='nsew', column=1, row=2, ipady=10, ipadx=10)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(column=2, row=2, sticky='ns')
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<Double-1>', self.changePathByClick)
        self.listbox.bind('<Return>', self.changePathByClick)

        # Status Bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(sticky='ew', column=0, row=3, columnspan=3)

        # Context Menu
        context_menu = tk.Menu(self, tearoff=0, background='#000000', foreground='#00FFFF', font=('Exo', 10))
        context_menu.add_command(label="Copy", command=self.copySelected)
        context_menu.add_command(label="Paste", command=self.pasteClipboard)
        context_menu.add_command(label="Delete", command=self.deleteSelected)
        context_menu.add_command(label="Rename", command=self.renameSelected)
        context_menu.add_command(label="Properties", command=self.showProperties)  # Properties option
        self.listbox.bind("<Button-3>", lambda event: self.show_context_menu(event, context_menu))

    def pathChange(self, *args):
        try:
            # Update file listbox based on the current path
            directory = os.listdir(self.currentPath.get())
            self.listbox.delete(0, tk.END)
            for file in directory:
                icon = "📄" if os.path.isfile(os.path.join(self.currentPath.get(), file)) else "📁"
                self.listbox.insert(tk.END, f"{icon} {file}")
            self.status_var.set(f"Current Path: {self.currentPath.get()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def changePathByClick(self, event=None):
        try:
            picked = self.listbox.get(self.listbox.curselection()[0]).strip("📄📁 ")
            path = os.path.join(self.currentPath.get(), picked)
            if os.path.isfile(path):
                os.startfile(path)
            else:
                self.currentPath.set(path)
                self.pathChange()  # Refresh the listbox for the new path
        except IndexError:
            pass

    def goBack(self, event=None):
        newPath = pathlib.Path(self.currentPath.get()).parent
        self.currentPath.set(newPath)
        self.pathChange()  # Refresh the listbox for the new path

    def searchFiles(self):
        query = self.searchQuery.get().lower()
        directory = os.listdir(self.currentPath.get())
        self.listbox.delete(0, tk.END)
        for file in directory:
            if query in file.lower():
                icon = "📄" if os.path.isfile(os.path.join(self.currentPath.get(), file)) else "📁"
                self.listbox.insert(tk.END, f"{icon} {file}")

    def searchDirectory(self):
        path = self.currentPath.get()
        if os.path.isdir(path):
            self.pathChange()  # Refresh the listbox for the new directory
        else:
            messagebox.showerror("Error", "The path specified is not a valid directory.")

    def openCreatePopup(self):
        top = tk.Toplevel(self)
        top.title("Create New")
        top.geometry("300x150")
        top.resizable(False, False)
        top.configure(bg='#000000')

        ttk.Label(top, text="Enter file or folder name:").grid(pady=10)
        entry = ttk.Entry(top, textvariable=self.newFileName)
        entry.grid(sticky='nsew', padx=10, pady=10)
        ttk.Button(top, text="Create", command=lambda: self.createFileOrFolder(top)).grid(sticky='nsew', padx=10, pady=10)

    def createFileOrFolder(self, top):
        name = self.newFileName.get()
        path = os.path.join(self.currentPath.get(), name)
        try:
            if '.' in name:
                open(path, 'w').close()
            else:
                os.mkdir(path)
            self.pathChange()
            top.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def showProperties(self):
        try:
            picked = self.listbox.get(self.listbox.curselection()[0]).strip("📄📁 ")
            path = os.path.join(self.currentPath.get(), picked)
            stats = os.stat(path)
            size = stats.st_size
            creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_ctime))
            modification_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))

            messagebox.showinfo("Properties", f"Name: {picked}\nPath: {path}\nSize: {size} bytes\nCreated: {creation_time}\nModified: {modification_time}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copySelected(self):
        try:
            picked = self.listbox.get(self.listbox.curselection()[0]).strip("📄📁 ")
            self.clipboard = os.path.join(self.currentPath.get(), picked)
        except IndexError:
            pass

    def pasteClipboard(self):
        if self.clipboard:
            dest = os.path.join(self.currentPath.get(), os.path.basename(self.clipboard))
            try:
                if os.path.isfile(self.clipboard):
                    shutil.copy2(self.clipboard, dest)
                else:
                    shutil.copytree(self.clipboard, dest)
                self.pathChange()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def deleteSelected(self):
        try:
            picked = self.listbox.get(self.listbox.curselection()[0]).strip("📄📁 ")
            path = os.path.join(self.currentPath.get(), picked)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            self.pathChange()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def renameSelected(self):
        try:
            picked = self.listbox.get(self.listbox.curselection()[0]).strip("📄📁 ")
            path = os.path.join(self.currentPath.get(), picked)
            new_name = simpledialog.askstring("Rename", "Enter new name:")
            if new_name:
                new_path = os.path.join(self.currentPath.get(), new_name)
                os.rename(path, new_path)
                self.pathChange()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_context_menu(self, event, context_menu):
        try:
            self.listbox.selection_set(self.listbox.nearest(event.y))
            context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Jungle")
    root.geometry("800x600")  
    root.configure(bg='#000000')

    # Configure the root window to expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    app = fexp(root)
    root.mainloop()
