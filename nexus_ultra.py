import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import serial
import serial.tools.list_ports
import time

# System Config
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NexusUltra(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER CONTROL")
        self.geometry("1200x750")

        # Layout Config
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (COMMAND CENTER) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="COMMANDS", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

        # Instant Launch Buttons
        self.add_sidebar_btn("FAST SCAN", self.run_nmap_fast)
        self.add_sidebar_btn("DEEP RECON", self.run_nmap_full)
        self.add_sidebar_btn("PACKET SNIFF", self.toggle_sniff)
        self.add_sidebar_btn("SYNC EARNINGS", self.sync_earnings)

        # Hardware Config Section
        ctk.CTkLabel(self.sidebar, text="HARDWARE HUB", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(40, 5))
        self.port_select = ctk.CTkOptionMenu(self.sidebar, values=["Searching Ports..."])
        self.port_select.pack(pady=10, padx=20)
        self.refresh_ports()

        self.add_sidebar_btn("CONNECT DEVICE", self.connect_serial, fg_color="#1e63d3")

        # --- MAIN INTERFACE ---
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        # Top Stats bar
        self.stats_frame = ctk.CTkFrame(self.main, height=60)
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.host_stat = ctk.CTkLabel(self.stats_frame, text="Active Hosts: 0", font=("Arial", 14))
        self.host_stat.pack(side="left", padx=30)
        self.earn_stat = ctk.CTkLabel(self.stats_frame, text="Daily Earnings: $0.00", font=("Arial", 14))
        self.earn_stat.pack(side="left", padx=30)

        # Data Table (Master View)
        self.tree_frame = ctk.CTkFrame(self.main)
        self.tree_frame.grid(row=1, column=0, sticky="nsew")
        
        style = ttk.Style()
        style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#1a1a1a", borderwidth=0, rowheight=30)
        style.map("Treeview", background=[('selected', '#1f538d')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ip", "name", "status", "vendor"), show='headings')
        for col in ("ip", "name", "status", "vendor"):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

        # Terminal Output
        self.console = ctk.CTkTextbox(self.main, height=200, font=("Courier", 12), fg_color="#000000", text_color="#00ff00")
        self.console.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.log("NEXUS SYSTEM INITIALIZED...")

    def add_sidebar_btn(self, text, cmd, fg_color=None):
        btn = ctk.CTkButton(self.sidebar, text=text, command=cmd, font=ctk.CTkFont(size=12, weight="bold"), fg_color=fg_color)
        btn.pack(pady=8, padx=20, fill="x")

    def log(self, text):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.console.see("end")

    # --- LOGIC FUNCTIONS ---

    def run_nmap_fast(self):
        self.log("Starting Rapid Scan (nmap -sn)...")
        threading.Thread(target=self.execute_nmap, args=("-sn 192.168.1.0/24",), daemon=True).start()

    def run_nmap_full(self):
        self.log("Starting Deep Recon (nmap -A)...")
        threading.Thread(target=self.execute_nmap, args=("-F 192.168.1.0/24",), daemon=True).start()

    def execute_nmap(self, args):
        try:
            # Note: Requires sudo or setcap on nmap
            cmd = f"nmap {args}"
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()
            
            # Simple Parser (In a real app, use python-nmap library)
            self.tree.delete(*self.tree.get_children())
            lines = output.split("\n")
            count = 0
            for line in lines:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(ip, "Discovered Host", "UP", "Unknown"))
                    count += 1
            
            self.host_stat.configure(text=f"Active Hosts: {count}")
            self.log(f"Scan Finished. Found {count} targets.")
        except Exception as e:
            self.log(f"ERROR: {e}")

    def refresh_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        if ports:
            self.port_select.configure(values=ports)
            self.port_select.set(ports[0])
        else:
            self.port_select.set("No Devices")

    def connect_serial(self):
        port = self.port_select.get()
        self.log(f"Attempting Serial Connection to {port}...")
        # Add actual serial read loop in a thread here

    def toggle_sniff(self): self.log("Tshark/Tcpdump Listener Triggered.")
    def sync_earnings(self): self.log("Fetching API data from Honeygain/Pawns...")

if __name__ == "__main__":
    app = NexusUltra()
    app.mainloop()
