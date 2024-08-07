import tkinter as tk
from tkinter import ttk
from fexp import fexp
from sh import sh
from coffee import coffee
from perfm import perfm
from MKD import MKD

class Project(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('')
        self.geometry('800x600')
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.frames = {
        'File Explorer': fexp(self.notebook), 
        'Shell': sh(self.notebook), 
        'Text Editor': coffee(self.notebook), 
        'Performance Monitor': perfm(self.notebook),
        "MKlang": MKD(self.notebook),
        }
        
        for name, frame in self.frames.items():
            self.notebook.add(frame, text=name)

if __name__ == '__main__':
    app = Project()
    app.mainloop()