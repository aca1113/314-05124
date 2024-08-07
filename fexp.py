
# file explorer
# not dependent on windows

import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pathlib
import shutil

class fexp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.currentPath = tk.StringVar(value=str(pathlib.Path.cwd()))
        self.newFileName = tk.StringVar(value="File.txt")
        self.currentPath.trace('w', self.pathChange)

        self.create_widgets()
        self.pathChange()

    def create_widgets(self):
        ttk.Button(self, text='Folder Up', command=self.goBack).grid(sticky='nsew', column=0, row=0)
        ttk.Entry(self, textvariable=self.currentPath).grid(sticky='nsew', column=1, row=0, ipady=10, ipadx=10)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=('Helvetica', 10))
        self.listbox.grid(sticky='nsew', column=1, row=1, ipady=10, ipadx=10)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(column=2, row=1, sticky='ns')
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<Double-1>', self.changePathByClick)
        self.listbox.bind('<Return>', self.changePathByClick)

        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(sticky='ew', column=0, row=2, columnspan=3)

        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Delete", command=self.deleteSelected)
        context_menu.add_command(label="Rename", command=self.renameSelected)
        self.listbox.bind("<Button-3>", lambda event: self.show_context_menu(event, context_menu))

    def pathChange(self, *args):
        try:
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
        except IndexError:
            pass

    def goBack(self, event=None):
        newPath = pathlib.Path(self.currentPath.get()).parent
        self.currentPath.set(newPath)

    def open_popup(self):
        top = tk.Toplevel(self)
        top.geometry("300x150")
        top.resizable(False, False)
        top.title("Create New")
        top.columnconfigure(0, weight=1)
        ttk.Label(top, text='Enter File or Folder name').grid(pady=10)
        ttk.Entry(top, textvariable=self.newFileName).grid(column=0, pady=10, sticky='nsew')
        ttk.Button(top, text="Create", command=lambda: self.newFileOrFolder(top)).grid(pady=10, sticky='nsew')

    def newFileOrFolder(self, top):
        new_path = os.path.join(self.currentPath.get(), self.newFileName.get())
        try:
            if '.' in self.newFileName.get():
                open(new_path, 'w').close()
            else:
                os.mkdir(new_path)
            top.destroy()
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
