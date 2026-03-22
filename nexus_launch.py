import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import serial.tools.list_ports
import time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NexusLaunch(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER CONTROL")
        self.geometry("1000x700")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="COMMANDS", font=("Arial", 16, "bold")).pack(pady=20)
        ctk.CTkButton(self.sidebar, text="QUICK SCAN", command=self.run_scan).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="REFRESH PORTS", command=self.refresh_ports).pack(pady=10, padx=20)

        # Main Area
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.tree = ttk.Treeview(self.main, columns=("ip", "status"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS")
        self.tree.heading("status", text="STATUS")
        self.tree.pack(fill="both", expand=True)

        self.console = ctk.CTkTextbox(self.main, height=200, fg_color="black", text_color="#00ff00")
        self.console.pack(fill="x", pady=(20, 0))

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.console.see("end")

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.log(f"Detected Ports: {ports}")

    def run_scan(self):
        self.log("Nmap started...")
        # Placeholder for real nmap integration
        self.tree.insert("", "end", values=("192.168.1.1", "ONLINE"))

if __name__ == "__main__":
    app = NexusLaunch()
    app.mainloop()
