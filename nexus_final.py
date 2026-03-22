import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess, threading, time, re

ctk.set_appearance_mode("Dark")

class NexusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER - V3.2")
        self.geometry("1000x700")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#0f0f12")
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="NEXUS RECON", font=("Courier", 20, "bold"), text_color="#00fbff").pack(pady=20)
        
        ctk.CTkLabel(self.sidebar, text="Target Subnet:").pack(pady=(10,0))
        self.target_entry = ctk.CTkEntry(self.sidebar, placeholder_text="192.168.12.0/24")
        self.target_entry.pack(pady=5, padx=10)
        self.target_entry.insert(0, "192.168.12.0/24") # Set to your actual subnet

        self.btn_recon = ctk.CTkButton(self.sidebar, text="RUN DISCOVERY", command=self.start_recon, fg_color="#1f538d")
        self.btn_recon.pack(pady=10, padx=20)

        # Main Panel
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.main, columns=("ip", "status", "ports"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS"); self.tree.heading("status", text="STATE"); self.tree.heading("ports", text="SERVICES")
        self.tree.column("ip", width=150); self.tree.column("status", width=100)
        self.tree.pack(fill="both", expand=True, pady=(0, 10))

        self.console = ctk.CTkTextbox(self.main, height=150, font=("Courier", 12), fg_color="black", text_color="#00ff00")
        self.console.pack(fill="x")

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] > {msg}\n")
        self.console.see("end")

    def start_recon(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        target = self.target_entry.get()
        self.log(f"Scanning Network: {target}")
        threading.Thread(target=self.run_nmap, args=(target,), daemon=True).start()

    def run_nmap(self, subnet):
        try:
            # -sn = Ping scan (fast), --unprivileged = Works better on Android
            proc = subprocess.Popen(["nmap", "-sn", "--unprivileged", subnet], stdout=subprocess.PIPE, text=True)
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(ip, "ACTIVE", "Discovered"))
                    self.log(f"HOST FOUND: {ip}")
            self.log("RECON COMPLETE.")
        except Exception as e: self.log(f"ERROR: {e}")

if __name__ == "__main__":
    NexusGUI().mainloop()
