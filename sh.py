import tkinter as tk
import subprocess
import os
import shutil

class sh(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.output_text = tk.Text(self, wrap="word", state="disabled", background="black", foreground="green")
        self.output_text.pack(fill="both", expand=True)
        
        self.command_entry = tk.Entry(self, background="black", foreground="green")
        self.command_entry.pack(fill="x")
        self.command_entry.bind("<Return>", self.execute_command)
        
        self.append_output("\nType commands below. Type 'help' for a list of commands.\n")

    def append_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.insert("end", text)
        self.output_text.see("end")
        self.output_text.config(state="disabled")

    def execute_command(self, event):
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, "end")
        
        if command:
            self.append_output(f"$ {command}\n")
            
            if command == "help":
                self.append_output(
                    "Available commands:\n"
                    "help - Display this help message\n"
                    "clear - Clear the screen\n"
                    "echo [text] - Echo text to the screen\n"
                    "cd [path] - Change directory\n"
                    "ls - List directory contents\n"
                    "pwd - Print working directory\n"
                    "cat [file] - Display file contents\n"
                    "touch [file] - Create an empty file\n"
                    "rm [file] - Remove a file\n"
                    "mkdir [dir] - Create a directory\n"
                    "rmdir [dir] - Remove a directory\n"
                    "cp [src] [dest] - Copy file\n"
                    "mv [src] [dest] - Move or rename file\n"
                    "exit - Exit the shell\n"
                )
            elif command == "clear":
                self.output_text.config(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.config(state="disabled")
            elif command.startswith("echo "):
                self.append_output(command[5:] + "\n")
            elif command.startswith("cd "):
                path = command[3:].strip()
                if not path:
                    path = os.path.expanduser("~")
                try:
                    os.chdir(path)
                    self.append_output(f"Changed directory to: {os.getcwd()}\n")
                except Exception as e:
                    self.append_output(f"cd: {str(e)}\n")
            elif command == "ls":
                try:
                    output = subprocess.check_output("ls", shell=True, text=True)
                    self.append_output(output)
                except subprocess.CalledProcessError as e:
                    self.append_output(f"ls: {str(e)}\n")
            elif command == "pwd":
                self.append_output(f"{os.getcwd()}\n")
            elif command.startswith("cat "):
                filepath = command[4:].strip()
                try:
                    with open(filepath, 'r') as file:
                        self.append_output(file.read())
                except Exception as e:
                    self.append_output(f"cat: {str(e)}\n")
            elif command.startswith("touch "):
                filepath = command[6:].strip()
                try:
                    open(filepath, 'a').close()
                    self.append_output(f"File {filepath} created.\n")
                except Exception as e:
                    self.append_output(f"touch: {str(e)}\n")
            elif command.startswith("rm "):
                filepath = command[3:].strip()
                try:
                    os.remove(filepath)
                    self.append_output(f"File {filepath} removed.\n")
                except Exception as e:
                    self.append_output(f"rm: {str(e)}\n")
            elif command.startswith("mkdir "):
                dirpath = command[6:].strip()
                try:
                    os.makedirs(dirpath, exist_ok=True)
                    self.append_output(f"Directory {dirpath} created.\n")
                except Exception as e:
                    self.append_output(f"mkdir: {str(e)}\n")
            elif command.startswith("rmdir "):
                dirpath = command[6:].strip()
                try:
                    os.rmdir(dirpath)
                    self.append_output(f"Directory {dirpath} removed.\n")
                except Exception as e:
                    self.append_output(f"rmdir: {str(e)}\n")
            elif command.startswith("cp "):
                try:
                    src, dest = command[3:].split()
                    shutil.copy(src, dest)
                    self.append_output(f"Copied {src} to {dest}\n")
                except Exception as e:
                    self.append_output(f"cp: {str(e)}\n")
            elif command.startswith("mv "):
                try:
                    src, dest = command[3:].split()
                    shutil.move(src, dest)
                    self.append_output(f"Moved {src} to {dest}\n")
                except Exception as e:
                    self.append_output(f"mv: {str(e)}\n")
            elif command == "exit":
                self.quit()
            else:
                try:
                    output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
                    self.append_output(output)
                except subprocess.CalledProcessError as e:
                    self.append_output(f"{e.output}\n")
                except Exception as e:
                    self.append_output(f"Command not found: {command}\n")

    def quit(self):
        self.append_output("Exiting shell...\n")
        self.master.quit()

