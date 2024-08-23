import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import json
import os

# Directory where the JSON files will be saved
SAVE_DIR = "sequoya_chunks"

# Ensure the save directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class Sequencer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sequoya")
        self.geometry("600x500")
        self.configure(bg="#1f1f1f")  
        self.create_widgets()
        self.hashed_string = ""

    def create_widgets(self):
        self.text_vars = []
        
        # Create 10 text bars
        for i in range(10):
            text_var = tk.StringVar()
            entry = tk.Entry(self, textvariable=text_var, width=50, bg="#2f2f2f", fg="#00FF00", insertbackground="#00FF00")
            entry.grid(row=i, column=0, padx=10, pady=5)
            self.text_vars.append(text_var)
        
        # Dropdown menus for input and output formats
        self.input_format = tk.StringVar(value="hash")
        self.output_format = tk.StringVar(value="hash")
        
        input_label = tk.Label(self, text="input method:", bg="#1f1f1f", fg="#FFFFFF")
        input_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.input_menu = ttk.Combobox(self, textvariable=self.input_format, values=["hash", "hex", "binary", "string", "int"])
        self.input_menu.grid(row=10, column=0, padx=110, pady=5)
        
        output_label = tk.Label(self, text="Output method:", bg="#1f1f1f", fg="#FFFFFF")
        output_label.grid(row=11, column=0, sticky="w", padx=10, pady=5)
        self.output_menu = ttk.Combobox(self, textvariable=self.output_format, values=["hash", "hex", "binary", "string", "int"])
        self.output_menu.grid(row=11, column=0, padx=110, pady=5)

        # Button to sequence
        self.sequence_button = tk.Button(self, text="Sequence", command=self.sequence, bg="#333333", fg="#00FF00")
        self.sequence_button.grid(row=12, column=0, padx=10, pady=5)

        # Text box to enter the file name
        self.file_name_var = tk.StringVar(value="")
        file_name_label = tk.Label(self, text="File Name:", bg="#1f1f1f", fg="#FFFFFF")
        file_name_label.grid(row=13, column=0, sticky="w", padx=10, pady=5)
        self.file_name_entry = tk.Entry(self, textvariable=self.file_name_var, width=50, bg="#2f2f2f", fg="#00FF00", insertbackground="#00FF00")
        self.file_name_entry.grid(row=13, column=0, padx=110, pady=5)

        # Button to save
        self.save_button = tk.Button(self, text="Save", command=self.save, bg="#333333", fg="#00FF00")
        self.save_button.grid(row=14, column=0, padx=10, pady=5)

        # Text box to display the resulting chunk
        self.result_box = tk.Text(self, height=5, width=60, bg="#2f2f2f", fg="#00FF00", insertbackground="#00FF00")
        self.result_box.grid(row=15, column=0, padx=10, pady=10)

    def sequence(self):
        inputs = [var.get()[:21] for var in self.text_vars]  # Get the inputs and limit to 21 characters
        combined_string = ''.join(inputs)  # Combine the inputs

        # Convert based on input format
        if self.input_format.get() == "hash":
            self.hashed_string = hashlib.sha256(combined_string.encode()).hexdigest()
        elif self.input_format.get() == "hex":
            self.hashed_string = combined_string.encode().hex().upper()            
        elif self.input_format.get() == "binary":
            self.hashed_string = ''.join(format(ord(c), '08b') for c in combined_string)
        elif self.input_format.get() == "string":
            self.hashed_string = combined_string
        elif self.input_format.get() == "int":
            self.hashed_string = str(sum(ord(c) for c in combined_string))

        # Convert to output format
        output = self.convert_output(self.hashed_string)

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, output)  # Display the converted output

    def convert_output(self, data):
        if self.output_format.get() == "hash":
            return hashlib.sha256(data.encode()).hexdigest()
        elif self.output_format.get() == "hex":
            return data.encode().hex().upper()  
        elif self.output_format.get() == "binary":
            return ''.join(format(ord(c), '08b') for c in data)
        elif self.output_format.get() == "string":
            return data
        elif self.output_format.get() == "int":
            return str(int.from_bytes(data.encode(), 'big'))
        return data

    def save(self):
        if self.hashed_string:
            # Save the result in a JSON file
            file_name = f"{self.file_name_var.get()}.json"
            result_file = os.path.join(SAVE_DIR, file_name)
            output = self.convert_output(self.hashed_string)
            with open(result_file, 'w') as f:
                json.dump({"output": output}, f)
            
        else:
            messagebox.showwarning("No Sequence", "Please sequence the inputs before saving.")

if __name__ == "__main__":
    app = Sequencer()
    app.mainloop()
