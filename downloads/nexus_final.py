import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import serial.tools.list_ports
import time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NexusFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER CONTROL - V1.0")
        self.geometry("1100x750")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="AUTO-TOOLS", font=("Courier", 18, "bold")).pack(pady=20)
        self.add_btn("LIVE NETWORK SCAN", self.start_nmap_thread)
        self.port_menu = ctk.CTkOptionMenu(self.sidebar, values=["Scanning..."])
        self.port_menu.pack(pady=10, padx=20)
        self.add_btn("REFRESH PORTS", self.refresh_ports)

        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.tree = ttk.Treeview(self.main, columns=("ip", "status"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS")
        self.tree.heading("status", text="STATUS")
        self.tree.pack(fill="both", expand=True)

        self.console = ctk.CTkTextbox(self.main, height=200, font=("Courier", 12), fg_color="#000000", text_color="#00ff00")
        self.console.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.refresh_ports()

    def add_btn(self, text, cmd):
        btn = ctk.CTkButton(self.sidebar, text=text, command=cmd)
        btn.pack(pady=6, padx=20, fill="x")

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.console.see("end")

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu.configure(values=ports if ports else ["No Ports"])
        self.log(f"Ports Refreshed: {len(ports)} found")

    def start_nmap_thread(self):
        self.log("Starting Network Scan...")
        threading.Thread(target=self.run_nmap, daemon=True).start()

    def run_nmap(self):
        try:
            cmd = "nmap -sn 192.168.1.0/24"
            proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, text=True)
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(ip, "ONLINE"))
            self.log("Scan Finished.")
        except Exception as e: self.log(f"Error: {e}")

if __name__ == "__main__":
    app = NexusFinal()
    app.mainloop()
