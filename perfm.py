# perfm.py
import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class perfm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Set up layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Information Text Box
        self.info_frame = ttk.LabelFrame(self, text="System Information")
        self.info_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.info_text = tk.Text(self.info_frame, height=5, wrap='word', state='disabled', bg='lightgray', fg='black', font=('Arial', 10))
        self.info_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Frame for Charts
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Set up charts
        self.fig, (self.cpu_ax, self.mem_ax, self.disk_ax, self.net_ax) = plt.subplots(4, 1, figsize=(8, 10))
        self.fig.tight_layout(pad=3.0)
        
        # Embed the chart in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Data containers
        self.cpu_data = [[] for _ in range(psutil.cpu_count(logical=True))]
        self.mem_data = []
        self.disk_data = []
        self.net_data = {'upload': [], 'download': []}

        # Initialize plots
        self.init_plots()
        self.update_info()
        self.update_monitor()
    
    def init_plots(self):
        # CPU Usage Plot
        self.cpu_lines = []
        for i in range(len(self.cpu_data)):
            line, = self.cpu_ax.plot([], [], label=f'Core {i + 1}')
            self.cpu_lines.append(line)
        self.cpu_ax.set_title('CPU Usage')
        self.cpu_ax.set_ylabel('Usage (%)')
        self.cpu_ax.legend(loc='upper right')

        # Memory Usage Plot
        self.mem_line, = self.mem_ax.plot([], [])
        self.mem_ax.set_title('Memory Usage')
        self.mem_ax.set_ylabel('Usage (GB)')

        # Disk Usage Plot
        self.disk_line, = self.disk_ax.plot([], [])
        self.disk_ax.set_title('Disk Usage')
        self.disk_ax.set_ylabel('Usage (GB)')

        # Network Performance Plot
        self.net_line_up, = self.net_ax.plot([], [], label='Upload')
        self.net_line_down, = self.net_ax.plot([], [], label='Download')
        self.net_ax.set_title('Network Performance')
        self.net_ax.set_ylabel('Speed (KB/s)')
        self.net_ax.legend(loc='upper right')
        
    def update_info(self):
        # Get system information
        cpu_info = f"CPU Cores: {psutil.cpu_count(logical=True)}\n"
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        net_info = psutil.net_if_addrs()
        
        info_text = cpu_info + \
                    f"Total Memory: {memory_info.total / (1024 ** 3):.2f} GB\n" + \
                    f"Total Disk: {disk_info.total / (1024 ** 3):.2f} GB\n" + \
                    "Network Interfaces:\n"

        for interface, addresses in net_info.items():
            for address in addresses:
                if address.family == 2:  # AF_INET (IPv4)
                    info_text += f"  - {interface}: {address.address}\n"
        
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state='disabled')

    def update_monitor(self):
        # Update CPU data
        cpu_percents = psutil.cpu_percent(percpu=True)
        for i, percent in enumerate(cpu_percents):
            self.cpu_data[i].append(percent)
            if len(self.cpu_data[i]) > 100:
                self.cpu_data[i].pop(0)
            self.cpu_lines[i].set_data(range(len(self.cpu_data[i])), self.cpu_data[i])
        
        # Update Memory data
        virtual_memory = psutil.virtual_memory()
        self.mem_data.append(virtual_memory.used / (1024 ** 3))
        if len(self.mem_data) > 100:
            self.mem_data.pop(0)
        self.mem_line.set_data(range(len(self.mem_data)), self.mem_data)
        
        # Update Disk data
        disk_usage = psutil.disk_usage('/')
        self.disk_data.append(disk_usage.used / (1024 ** 3))
        if len(self.disk_data) > 100:
            self.disk_data.pop(0)
        self.disk_line.set_data(range(len(self.disk_data)), self.disk_data)
        
        # Update Network data
        net_io = psutil.net_io_counters()
        upload_speed = net_io.bytes_sent
        download_speed = net_io.bytes_recv
        # Calculate speed over a period of time
        self.after(1000, self.calculate_net_speed, upload_speed, download_speed)
        
        # Redraw the plots
        self.cpu_ax.relim()
        self.cpu_ax.autoscale_view()
        self.mem_ax.relim()
        self.mem_ax.autoscale_view()
        self.disk_ax.relim()
        self.disk_ax.autoscale_view()
        self.net_ax.relim()
        self.net_ax.autoscale_view()
        
        self.canvas.draw()

    def calculate_net_speed(self, upload_speed, download_speed):
        new_net_io = psutil.net_io_counters()
        upload_speed = (new_net_io.bytes_sent - upload_speed) / 1024
        download_speed = (new_net_io.bytes_recv - download_speed) / 1024
        
        self.net_data['upload'].append(upload_speed)
        self.net_data['download'].append(download_speed)
        
        if len(self.net_data['upload']) > 100:
            self.net_data['upload'].pop(0)
            self.net_data['download'].pop(0)
        
        self.net_line_up.set_data(range(len(self.net_data['upload'])), self.net_data['upload'])
        self.net_line_down.set_data(range(len(self.net_data['download'])), self.net_data['download'])

        # Schedule the next update
        self.after(1000, self.update_monitor)
