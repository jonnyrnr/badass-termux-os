import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MinimalNexus(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus Control")
        self.geometry("1100x650")

        # Create 1x2 Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR NAV ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NEXUS OS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Instant Launch Buttons
        self.btn_scan = ctk.CTkButton(self.sidebar_frame, text="Network Scan", command=self.placeholder_action)
        self.btn_scan.grid(row=1, column=0, padx=20, pady=10)

        self.btn_packets = ctk.CTkButton(self.sidebar_frame, text="Packet Capture", command=self.placeholder_action)
        self.btn_packets.grid(row=2, column=0, padx=20, pady=10)

        self.btn_earn = ctk.CTkButton(self.sidebar_frame, text="Automation Sync", command=self.placeholder_action)
        self.btn_earn.grid(row=3, column=0, padx=20, pady=10)

        # Device Config Quick-Select
        self.dev_label = ctk.CTkLabel(self.sidebar_frame, text="DEVICE CONNECT", font=ctk.CTkFont(size=12))
        self.dev_label.grid(row=5, column=0, padx=20, pady=(100, 0))
        
        self.device_opt = ctk.CTkOptionMenu(self.sidebar_frame, values=["ESP32 WROOM", "RasPi 3", "Arduino Uno", "Pi Pico"])
        self.device_opt.grid(row=6, column=0, padx=20, pady=10)

        # --- MAIN CONTENT AREA ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Top Stats Bar
        self.stats_frame = ctk.CTkFrame(self.main_content, height=80)
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Simple Labels for Stats
        self.stat1 = ctk.CTkLabel(self.stats_frame, text="Active Hosts: 12", padx=20).pack(side="left")
        self.stat2 = ctk.CTkLabel(self.stats_frame, text="Uptime: 99.8%", padx=20).pack(side="left")
        self.stat3 = ctk.CTkLabel(self.stats_frame, text="Earnings: $4.20", padx=20).pack(side="left")

        # Master Data Table (Using standard Treeview for data density)
        self.table_container = ctk.CTkFrame(self.main_content)
        self.table_container.grid(row=1, column=0, sticky="nsew")
        
        columns = ("device", "ip", "status", "activity")
        self.tree = ttk.Treeview(self.table_container, columns=columns, show='headings')
        self.tree.heading("device", text="DEVICE")
        self.tree.heading("ip", text="IP ADDRESS")
        self.tree.heading("status", text="STATUS")
        self.tree.heading("activity", text="LAST ACTIVITY")
        
        # Styling the Treeview to match Dark Mode
        style = ttk.Style()
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.insert("", "end", values=("RasPi 3", "192.168.1.15", "Active", "Scanning..."))
        self.tree.insert("", "end", values=("ESP32", "192.168.1.22", "Idle", "N/A"))

        # Bottom Console (Clean & Uncluttered)
        self.textbox = ctk.CTkTextbox(self.main_content, height=150)
        self.textbox.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.textbox.insert("0.0", "System Ready...\nLogged in as Kali Admin.\n")

    def placeholder_action(self):
        self.textbox.insert("end", "Executing command...\n")

if __name__ == "__main__":
    app = MinimalNexus()
    app.mainloop()
