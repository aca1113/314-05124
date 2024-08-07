import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
import re

class MKD(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.text_widget = ScrolledText(self, wrap='word', font=("Courier", 12))
        self.text_widget.pack(fill='both', expand=True)
        
        toolbar = tk.Frame(self)
        toolbar.pack(fill='x')

        save_button = tk.Button(toolbar, text="Save", command=self.save_to_file)
        save_button.pack(side='left')
        load_button = tk.Button(toolbar, text="Load", command=self.load_from_file)
        load_button.pack(side='left')

        bold_button = tk.Button(toolbar, text="B", command=lambda: self.apply_tag("**"))
        bold_button.pack(side='left')
        italic_button = tk.Button(toolbar, text="I", command=lambda: self.apply_tag("*"))
        italic_button.pack(side='left')
        strikethrough_button = tk.Button(toolbar, text="S", command=lambda: self.apply_tag("~~"))
        strikethrough_button.pack(side='left')
        code_button = tk.Button(toolbar, text="Code", command=lambda: self.apply_tag("`"))
        code_button.pack(side='left')
        heading_button = tk.Button(toolbar, text="H", command=lambda: self.apply_heading("#"))
        heading_button.pack(side='left')

        self.text_widget.bind('<KeyRelease>', self.highlight_syntax)
        
        sample_content = (
            "## Features\n"
            "- **Bold Text**\n"
            "- *Italic Text*\n"
            "- ~~Strikethrough~~\n"
            "- `Inline Code`\n"
            "```\n"
            "Code Block\n"
            "```\n"
            "> Quotes are supported too.\n"
            "[Link](https://www.example.com)\n"
            "![Image](https://www.example.com/image.jpg)\n"
            "| Header 1 | Header 2 |\n"
            "|----------|----------|\n"
            "| Cell 1   | Cell 2   |\n"
            "~~Deleted Text~~\n"
            "[Email](mailto:example@example.com)\n"
        )
        self.text_widget.insert("1.0", sample_content)
        self.highlight_syntax()

    def apply_tag(self, tag):
        try:
            start = self.text_widget.index(tk.SEL_FIRST)
            end = self.text_widget.index(tk.SEL_LAST)
            text = self.text_widget.get(start, end)
            self.text_widget.delete(start, end)
            self.text_widget.insert(start, f"{tag}{text}{tag}")
        except tk.TclError:
            pass

    def apply_heading(self, prefix):
        try:
            line_start = self.text_widget.index(tk.SEL_FIRST).split('.')[0]
            self.text_widget.insert(f"{line_start}.0", f"{prefix} ")
        except tk.TclError:
            pass

    def highlight_syntax(self, event=None):
        self.text_widget.tag_remove("highlight", "1.0", tk.END)

        self.text_widget.tag_configure("heading", foreground="blue", font=("Courier", 14, "bold"))
        self.text_widget.tag_configure("bold", foreground="darkred", font=("Courier", 12, "bold"))
        self.text_widget.tag_configure("italic", foreground="darkgreen", font=("Courier", 12, "italic"))
        self.text_widget.tag_configure("strikethrough", font=("Courier", 12, "overstrike"))
        self.text_widget.tag_configure("bullet", foreground="black", font=("Courier", 12))
        self.text_widget.tag_configure("quote", foreground="gray", font=("Courier", 12, "italic"))
        self.text_widget.tag_configure("inline_code", foreground="purple", font=("Courier", 12, "italic"))
        self.text_widget.tag_configure("code_block", background="#f0f0f0", foreground="black")
        self.text_widget.tag_configure("link", foreground="blue", underline=True)
        self.text_widget.tag_configure("image", foreground="orange")
        self.text_widget.tag_configure("email", foreground="blue", underline=True)

        patterns = {
            "heading": r"^(#{1,6})\s+.*$",
            "bold": r"\*\*(.+?)\*\*",
            "italic": r"\*(.+?)\*",
            "strikethrough": r"~~(.+?)~~",
            "bullet": r"^- .*$",
            "quote": r"^> .*$",
            "code_block": r"```[\s\S]+?```",
            "inline_code": r"`(.+?)`",
            "link": r"\[([^\]]+)\]\((https?://[^\)]+)\)",
            "image": r"!\[([^\]]*)\]\(([^)]+)\)",
            "email": r"\[([^\]]+)\]\((mailto:[^)]+)\)",
            "table": r"^\|(.+)\|\n^\|(?:-+\|)+\n(?:^\|(.+)\|\n)*",
        }

        for tag, pattern in patterns.items():
            start_idx = "1.0"
            while True:
                match = re.search(pattern, self.text_widget.get(start_idx, tk.END), re.MULTILINE)
                if not match:
                    break
                start, end = match.span()
                line_start, col_start = map(int, self.text_widget.index(f"{start_idx}+{start}c").split('.'))
                line_end, col_end = map(int, self.text_widget.index(f"{start_idx}+{end}c").split('.'))
                start_idx = f"{line_start}.{col_start}"
                end_idx = f"{line_end}.{col_end}"
                self.text_widget.tag_add(tag, start_idx, end_idx)
                start_idx = end_idx

    def get_content(self):
        return self.text_widget.get("1.0", tk.END)

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mk", filetypes=[("MK Files", "*.mk"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.get_content())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def load_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("MK Files", "*.mk"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert("1.0", content)
                self.highlight_syntax()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
