        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="STATS", font=("Courier", 16, "bold")).pack(pady=20)
        self.stat_label = ctk.CTkLabel(self.sidebar, text="Hosts: 0\nPorts: 0", justify="left")
        self.stat_label.pack(pady=10)

        # Main Control Area
        self.main = ctk.CTkFrame(self)
        self.main.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.lbl = ctk.CTkLabel(self.main, text="COMMAND CENTER", font=("Courier", 22, "bold"), text_color="#00fbff")
        self.lbl.pack(pady=10)
        
        self.btn_scan = ctk.CTkButton(self.main, text="DEEP RECON SCAN", command=self.start_scan, fg_color="#1f538d")
        self.btn_scan.pack(pady=5)

        # Terminal Output
        self.console = ctk.CTkTextbox(self.main, font=("Courier", 13), fg_color="#0a0a0a", text_color="#00ff00", border_width=1)
        self.console.pack(padx=10, pady=10, fill="both", expand=True)

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.console.see("end")

    def get_subnet(self):
        try:
            route = subprocess.check_output(["ip", "route"]).decode()
            match = re.search(r"(\d+\.\d+\.\d+\.0/\d+)", route)
            return match.group(1) if match else "192.168.1.0/24"
        except: return "192.168.1.0/24"

    def start_scan(self):
        self.console.delete("1.0", "end")
        self.log("Initializing Nmap Engine...")
        subnet = self.get_subnet()
        threading.Thread(target=self.run_deep_scan, args=(subnet,), daemon=True).start()

    def run_deep_scan(self, subnet):
        host_count = 0
        port_count = 0
        try:
            # -F (Fast scan 100 ports), -T4 (Aggressive speed), --open (Only active)
            proc = subprocess.Popen(["nmap", "-F", "-T4", "--open", subnet], stdout=subprocess.PIPE, text=True)
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    self.log(f"FOUND HOST: {ip}")
                    host_count += 1
                if "/tcp" in line and "open" in line:
                    self.log(f"  [!] Port {line.strip()}")
                    port_count += 1
                self.stat_label.configure(text=f"Hosts: {host_count}\nPorts: {port_count}")
            self.log("RECON COMPLETE.")
        except Exception as e:
            self.log(f"ERROR: {e}")

if __name__ == "__main__":
    app = Nexus()
    app.mainloop()
EOF

kill -9 -f termux-x11; pkill -9 -f python
rm -f /data/data/com.termux/files/usr/tmp/.X1-lock
rm -rf /data/data/com.termux/files/usr/tmp/.X11-unix
termux-x11 :1 &
export DISPLAY=:1; python3 nexus_final.py
cat << 'EOF' > nexus_final.py
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
EOF

python3 nexus_final.py
cat << 'EOF' > nexus_final.py
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess, threading, time, re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NexusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER CONTROL - V3.0")
        self.geometry("1000x700")

        # --- SIDEBAR (THE TOOLS) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0f0f12")
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="NEXUS OS", font=("Courier", 24, "bold"), text_color="#00fbff").pack(pady=20)
        
        self.btn_recon = ctk.CTkButton(self.sidebar, text="DEEP RECON", command=self.start_recon, fg_color="#1f538d")
        self.btn_recon.pack(pady=10, padx=20)
        
        self.btn_clear = ctk.CTkButton(self.sidebar, text="PURGE LOGS", command=self.clear_logs, fg_color="#333333")
        self.btn_clear.pack(pady=10, padx=20)

        self.stats = ctk.CTkLabel(self.sidebar, text="SYSTEM: ONLINE\nTARGETS: 0", justify="left", font=("Courier", 12))
        self.stats.pack(side="bottom", pady=20)

        # --- MAIN PANEL ---
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # 1. LIVE HOST TABLE (Restoring the Pro Look)
        self.table_frame = ctk.CTkFrame(self.main, fg_color="#1a1a1a")
        self.table_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#1a1a1a", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self.table_frame, columns=("ip", "status", "services"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS")
        self.tree.heading("status", text="STATUS")
        self.tree.heading("services", text="OPEN PORTS")
        self.tree.column("ip", width=150)
        self.tree.column("status", width=100)
        self.tree.pack(fill="both", expand=True)

        # 2. CONSOLE (The Hacker Feed)
        self.console = ctk.CTkTextbox(self.main, height=200, font=("Courier", 13), fg_color="#000000", text_color="#00ff00", border_color="#00fbff", border_width=1)
        self.console.pack(fill="x")

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] > {msg}\n")
        self.console.see("end")

    def clear_logs(self):
        self.console.delete("1.0", "end")
        for i in self.tree.get_children(): self.tree.delete(i)

    def get_active_subnet(self):
        try:
            # Better subnet detection for Android/Termux
            cmd = subprocess.check_output(["ip", "route"]).decode()
            match = re.search(r"(\d+\.\d+\.\d+\.0/\d+)", cmd)
            return match.group(1) if match else "192.168.1.0/24"
        except: return "192.168.1.0/24"

    def start_recon(self):
        self.log("Initializing Nmap Engine...")
        target = self.get_active_subnet()
        self.log(f"Subnet Detected: {target}")
        threading.Thread(target=self.run_nmap, args=(target,), daemon=True).start()

    def run_nmap(self, subnet):
        try:
            # -F = Fast Scan, -T4 = High speed
            proc = subprocess.Popen(["nmap", "-F", "-T4", "--open", subnet], stdout=subprocess.PIPE, text=True)
            current_ip = None
            
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    current_ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(current_ip, "ONLINE", "Scanning..."))
                    self.log(f"Host Discovered: {current_ip}")
                
                if "/tcp" in line and "open" in line:
                    port_info = line.split()[0]
                    # Update the last added item in the table
                    last_item = self.tree.get_children()[-1]
                    old_vals = self.tree.item(last_item, 'values')
                    new_ports = f"{old_vals[2]}, {port_info}".replace("Scanning..., ", "")
                    self.tree.item(last_item, values=(old_vals[0], old_vals[1], new_ports))
            
            self.log("RECON COMPLETE.")
        except Exception as e:
            self.log(f"ERROR: {str(e)}")

if __name__ == "__main__":
    app = NexusGUI()
    app.mainloop()
EOF

cat << 'EOF' > nexus_final.py
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess, threading, time, re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NexusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER CONTROL - V3.0")
        self.geometry("1000x700")

        # --- SIDEBAR (THE TOOLS) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0f0f12")
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="NEXUS OS", font=("Courier", 24, "bold"), text_color="#00fbff").pack(pady=20)
        
        self.btn_recon = ctk.CTkButton(self.sidebar, text="DEEP RECON", command=self.start_recon, fg_color="#1f538d")
        self.btn_recon.pack(pady=10, padx=20)
        
        self.btn_clear = ctk.CTkButton(self.sidebar, text="PURGE LOGS", command=self.clear_logs, fg_color="#333333")
        self.btn_clear.pack(pady=10, padx=20)

        self.stats = ctk.CTkLabel(self.sidebar, text="SYSTEM: ONLINE\nTARGETS: 0", justify="left", font=("Courier", 12))
        self.stats.pack(side="bottom", pady=20)

        # --- MAIN PANEL ---
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # 1. LIVE HOST TABLE (Restoring the Pro Look)
        self.table_frame = ctk.CTkFrame(self.main, fg_color="#1a1a1a")
        self.table_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#1a1a1a", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self.table_frame, columns=("ip", "status", "services"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS")
        self.tree.heading("status", text="STATUS")
        self.tree.heading("services", text="OPEN PORTS")
        self.tree.column("ip", width=150)
        self.tree.column("status", width=100)
        self.tree.pack(fill="both", expand=True)

        # 2. CONSOLE (The Hacker Feed)
        self.console = ctk.CTkTextbox(self.main, height=200, font=("Courier", 13), fg_color="#000000", text_color="#00ff00", border_color="#00fbff", border_width=1)
        self.console.pack(fill="x")

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] > {msg}\n")
        self.console.see("end")

    def clear_logs(self):
        self.console.delete("1.0", "end")
        for i in self.tree.get_children(): self.tree.delete(i)

    def get_active_subnet(self):
        try:
            # Better subnet detection for Android/Termux
            cmd = subprocess.check_output(["ip", "route"]).decode()
            match = re.search(r"(\d+\.\d+\.\d+\.0/\d+)", cmd)
            return match.group(1) if match else "192.168.1.0/24"
        except: return "192.168.1.0/24"

    def start_recon(self):
        self.log("Initializing Nmap Engine...")
        target = self.get_active_subnet()
        self.log(f"Subnet Detected: {target}")
        threading.Thread(target=self.run_nmap, args=(target,), daemon=True).start()

    def run_nmap(self, subnet):
        try:
            # -F = Fast Scan, -T4 = High speed
            proc = subprocess.Popen(["nmap", "-F", "-T4", "--open", subnet], stdout=subprocess.PIPE, text=True)
            current_ip = None
            
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    current_ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(current_ip, "ONLINE", "Scanning..."))
                    self.log(f"Host Discovered: {current_ip}")
                
                if "/tcp" in line and "open" in line:
                    port_info = line.split()[0]
                    # Update the last added item in the table
                    last_item = self.tree.get_children()[-1]
                    old_vals = self.tree.item(last_item, 'values')
                    new_ports = f"{old_vals[2]}, {port_info}".replace("Scanning..., ", "")
                    self.tree.item(last_item, values=(old_vals[0], old_vals[1], new_ports))
            
            self.log("RECON COMPLETE.")
        except Exception as e:
            self.log(f"ERROR: {str(e)}")

if __name__ == "__main__":
    app = NexusGUI()
    app.mainloop()
EOF

cd ~,/downloads
downloads
cd
ls
cat << 'EOF' > nexus_final.py
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess, threading, time, re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NexusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER CONTROL - V3.0")
        self.geometry("1000x700")
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0f0f12")
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="NEXUS OS", font=("Courier", 24, "bold"), text_color="#00fbff").pack(pady=20)
        self.btn_recon = ctk.CTkButton(self.sidebar, text="DEEP RECON", command=self.start_recon, fg_color="#1f538d")
        self.btn_recon.pack(pady=10, padx=20)
        self.btn_clear = ctk.CTkButton(self.sidebar, text="PURGE LOGS", command=self.clear_logs, fg_color="#333333")
        self.btn_clear.pack(pady=10, padx=20)
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.table_frame = ctk.CTkFrame(self.main, fg_color="#1a1a1a")
        self.table_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.tree = ttk.Treeview(self.table_frame, columns=("ip", "status", "services"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS"); self.tree.heading("status", text="STATUS"); self.tree.heading("services", text="OPEN PORTS")
        self.tree.pack(fill="both", expand=True)
        self.console = ctk.CTkTextbox(self.main, height=200, font=("Courier", 13), fg_color="#000000", text_color="#00ff00", border_color="#00fbff", border_width=1)
        self.console.pack(fill="x")

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] > {msg}\n")
        self.console.see("end")

    def clear_logs(self):
        self.console.delete("1.0", "end")
        for i in self.tree.get_children(): self.tree.delete(i)

    def get_active_subnet(self):
        try:
            cmd = subprocess.check_output(["ip", "route"]).decode()
            match = re.search(r"(\d+\.\d+\.\d+\.0/\d+)", cmd)
            return match.group(1) if match else "192.168.1.0/24"
        except: return "192.168.1.0/24"

    def start_recon(self):
        self.log("Initializing Nmap Engine...")
        target = self.get_active_subnet()
        threading.Thread(target=self.run_nmap, args=(target,), daemon=True).start()

    def run_nmap(self, subnet):
        try:
            proc = subprocess.Popen(["nmap", "-F", "-T4", "--open", subnet], stdout=subprocess.PIPE, text=True)
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(ip, "ONLINE", ""))
                    self.log(f"Host Discovered: {ip}")
                if "/tcp" in line and "open" in line:
                    port_info = line.split()[0]
                    last_item = self.tree.get_children()[-1]
                    old = self.tree.item(last_item, 'values')
                    self.tree.item(last_item, values=(old[0], old[1], f"{old[2]} {port_info}"))
            self.log("RECON COMPLETE.")
        except Exception as e: self.log(f"ERROR: {e}")

if __name__ == "__main__":
    NexusGUI().mainloop()
EOF

# KILL OLD STUFF
pkill -9 -f termux-x11; pkill -9 -f python
rm -rf $TMPDIR/.X11-unix
# START DISPLAY
termux-x11 :1 &
# WAIT A BEAT THEN RUN
sleep 2
export DISPLAY=:1
python3 nexus_final.py
cat << 'EOF' > nexus_final.py
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import subprocess, threading, time, re

ctk.set_appearance_mode("Dark")

class NexusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEXUS MASTER - V3.1")
        self.geometry("1000x700")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#0f0f12")
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="NEXUS RECON", font=("Courier", 20, "bold")).pack(pady=20)
        
        # Subnet Manual Entry
        ctk.CTkLabel(self.sidebar, text="Target Subnet:").pack(pady=(10,0))
        self.target_entry = ctk.CTkEntry(self.sidebar, placeholder_text="192.168.1.0/24")
        self.target_entry.pack(pady=5, padx=10)
        self.target_entry.insert(0, self.get_active_subnet())

        self.btn_recon = ctk.CTkButton(self.sidebar, text="RUN DISCOVERY", command=self.start_recon)
        self.btn_recon.pack(pady=20, padx=20)

        # Main Panel
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(self.main, columns=("ip", "status", "ports"), show='headings')
        self.tree.heading("ip", text="IP ADDRESS"); self.tree.heading("status", text="STATE"); self.tree.heading("ports", text="PORTS")
        self.tree.pack(fill="both", expand=True, pady=(0, 10))

        self.console = ctk.CTkTextbox(self.main, height=150, fg_color="black", text_color="#00ff00")
        self.console.pack(fill="x")

    def log(self, msg):
        self.console.insert("end", f"[{time.strftime('%H:%M:%S')}] > {msg}\n")
        self.console.see("end")

    def get_active_subnet(self):
        try:
            cmd = subprocess.check_output(["ip", "addr"]).decode()
            match = re.search(r"inet (192\.168\.\d+)\.", cmd)
            return f"{match.group(1)}.0/24" if match else "192.168.1.0/24"
        except: return "192.168.1.0/24"

    def start_recon(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        target = self.target_entry.get()
        self.log(f"Starting Scan on {target}...")
        threading.Thread(target=self.run_nmap, args=(target,), daemon=True).start()

    def run_nmap(self, subnet):
        try:
            # -sn = Ping scan, --send-ip = Use unprivileged mode for non-root
            proc = subprocess.Popen(["nmap", "-sn", "--send-ip", subnet], stdout=subprocess.PIPE, text=True)
            for line in proc.stdout:
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    self.tree.insert("", "end", values=(ip, "ACTIVE", "Pending..."))
                    self.log(f"Found: {ip}")
            self.log("Discovery Finished.")
        except Exception as e: self.log(f"ERROR: {e}")

if __name__ == "__main__":
    NexusGUI().mainloop()
EOF

