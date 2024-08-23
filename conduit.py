import tkinter as tk
import math
import os

class conduit:
    def __init__(self, root):
        self.root = root
        self.root.title("the conduit")

        # Define the size of the text box
        self.text_box_width = 30
        self.text_box_height = 15

        # Initial window size
        self.window_width = 800
        self.window_height = 600
        self.root.geometry(f'{self.window_width}x{self.window_height}')

        # Create a Canvas widget
        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a Text widget with specified size
        self.text_box = tk.Text(root, width=self.text_box_width, height=self.text_box_height)
        self.text_box.place(relx=0.5, rely=0.4, anchor=tk.CENTER,)

        # Create a Save button
        self.save_button = tk.Button(root, text="Save", width=self.text_box_width, command=self.save_file)
        self.save_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        # Parameters for the rings
        self.num_rings = 21
        self.radius = 300
        self.ring_radius = 20
        self.angle_step = 360 / self.num_rings
        self.rings = []
        self.angle = 0
        self.current_file = None  # Track the currently displayed file

        # Create directory and files
        self.create_files()

        # Draw initial rings
        self.draw_rings()

        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)

        # Start animation
        self.animate_rings()

    def create_files(self):
        directory = 'cnd'
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.file_paths = []  # Store file paths

        for i in range(1, self.num_rings + 1):
            file_name = f"{i}.cnd"
            file_path = os.path.join(directory, file_name)
            self.file_paths.append(file_path)

            # Create files with empty content
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    pass

    def on_resize(self, event):
        self.window_width = event.width
        self.window_height = event.height
        self.canvas.config(width=self.window_width, height=self.window_height)

        # Redraw background and rings
        self.create_gradient()
        self.draw_rings()

    def create_gradient(self):

        self.canvas.delete('gradient')  # Remove old gradient lines

        # Create a gradient using an image for better performance
        gradient_image = tk.PhotoImage(width=self.window_width, height=self.window_height)
        for i in range(self.window_height):
            r = int(255 - (255 * (i / self.window_height)))
            g = int(182 - (182 * (i / self.window_height)))
            b = 255
            color = f'#{r:02x}{g:02x}{b:02x}'
            gradient_image.put(color, (0, i, self.window_width, i + 1))

        self.canvas.create_image(0, 0, image=gradient_image, anchor=tk.NW, tags='gradient')
        self.canvas.image = gradient_image  # Keep a reference to prevent garbage collection

    def draw_rings(self):
        self.canvas.delete('ring')  # Remove old rings
        self.rings = []  # Clear previous rings

        for i in range(self.num_rings):
            angle = i * self.angle_step
            x = self.window_width / 2 + self.radius * math.cos(math.radians(angle))
            y = self.window_height / 2 + self.radius * math.sin(math.radians(angle))
            file_name = os.path.basename(self.file_paths[i])
            ring = self.canvas.create_oval(
                x - self.ring_radius, y - self.ring_radius,
                x + self.ring_radius, y + self.ring_radius,
                outline='lightblue', width=2, tags='ring'
            )
            text = self.canvas.create_text(
                x, y, text=file_name, fill='black', tags='ring'
            )
            self.rings.append((ring, text, self.file_paths[i]))

        # Bind click event
        self.canvas.tag_bind('ring', '<Button-1>', self.on_ring_click)

    def on_ring_click(self, event):

        item = self.canvas.find_closest(event.x, event.y)[0]
        for ring, text, file_path in self.rings:
            if item == ring or item == text:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.text_box.delete('1.0', tk.END)
                self.text_box.insert(tk.END, content)
                self.current_file = file_path
                break

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as f:
                content = self.text_box.get('1.0', tk.END)
                f.write(content.strip())
            print(f"File '{self.current_file}' saved.")

    def animate_rings(self):
        self.angle += 1
        if self.angle >= 360:
            self.angle = 0

        for i, (ring, text, _) in enumerate(self.rings):
            angle = (i * self.angle_step + self.angle) % 360
            x = self.window_width / 2 + self.radius * math.cos(math.radians(angle))
            y = self.window_height / 2 + self.radius * math.sin(math.radians(angle))
            self.canvas.coords(
                ring,
                x - self.ring_radius, y - self.ring_radius,
                x + self.ring_radius, y + self.ring_radius
            )
            self.canvas.coords(
                text,
                x, y
            )
        
        self.canvas.update_idletasks()  # Explicitly request an update
        self.root.after(50, self.animate_rings)  # Adjust the interval for performance

if __name__ == "__main__":
    root = tk.Tk()
    app = conduit(root)
    root.mainloop()
