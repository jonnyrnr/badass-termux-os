import streamlit as st
import pandas as pd
import subprocess
import os

st.set_page_config(page_title="KALI OMNI-HUB: GOD MODE", layout="wide")
st.title("💀 KALI OMNI-HUB: TOTAL COMMAND")

# --- SIDEBAR: SYSTEM & OSINT ---
st.sidebar.header("🔍 OSINT & System")
ip_lookup = st.sidebar.text_input("IP/Domain Lookup")
if st.sidebar.button("Whois"):
    res = subprocess.run(["whois", ip_lookup], capture_output=True, text=True)
    st.sidebar.code(res.stdout)

# --- THE KITCHEN SINK TABS ---
t1, t2, t3, t4, t5 = st.tabs(["📡 Recon", "🌐 Web Audit", "🔓 Cracking", "💣 Exploits", "📶 Wireless"])

with t1:
    st.header("Nmap Network Mapping")
    target = st.text_input("Target Range", "192.168.1.0/24")
    if st.button("🚀 Execute Nmap"):
        res = subprocess.run(["nmap", "-A", target], capture_output=True, text=True)
        st.code(res.stdout)

with t2:
    st.header("Nikto Web Audit")
    web_target = st.text_input("URL", "http://127.0.0.1")
    if st.button("🔍 Run Nikto"):
        res = subprocess.run(["nikto", "-h", web_target], capture_output=True, text=True)
        st.code(res.stdout)

with t3:
    st.header("John the Ripper")
    if st.button("📊 Show Cracked"):
        res = subprocess.run(["john", "--show", "temp_hash.txt"], capture_output=True, text=True)
        st.code(res.stdout)

with t4:
    st.header("Searchsploit")
    query = st.text_input("Search Exploit-DB")
    if st.button("🔎 Find"):
        res = subprocess.run(["searchsploit", query], capture_output=True, text=True)
        st.code(res.stdout)

with t5:
    st.header("Wireless Warfare (Aircrack-ng)")
    interface = st.text_input("Wireless Interface", "wlan0mon")
    if st.button("📡 Monitor Mode On"):
        os.system(f"airmon-ng start {interface}")
        st.success(f"{interface} enabled in Monitor Mode.")
    if st.button("🕵️ Scan for APs"):
        st.info("Starting airodump-ng... output will save to capture.csv")
        subprocess.Popen(["sudo", "airodump-ng", "-w", "capture", "--output-format", "csv", interface])
