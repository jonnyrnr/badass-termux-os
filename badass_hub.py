import streamlit as st
import pandas as pd
import subprocess
import psutil
import os

st.set_page_config(page_title="KALI GUI: PHOENIX", layout="wide")
st.title("🛡️ KALI OFFENSIVE DASHBOARD")

# --- SIDEBAR: SYSTEM VITALS ---
st.sidebar.header("📡 Node Status")
st.sidebar.metric("CPU", f"{psutil.cpu_percent()}%")
if st.sidebar.button("💀 SHUTDOWN HUB"):
    os._exit(0)

# --- TABBED INTERFACE ---
tab1, tab2 = st.tabs(["🔍 Network Recon", "🔓 Password Cracking"])

with tab1:
    st.header("Network Discovery")
    target = st.text_input("Target Range", "192.168.1.0/24")
    if st.button("🚀 Run Nmap Scan"):
        with st.spinner("Scanning..."):
            result = subprocess.run(["nmap", "-sV", "-T4", target], capture_output=True, text=True)
            st.code(result.stdout)

with tab2:
    st.header("John the Ripper Interface")
    hash_file = st.file_uploader("Upload Hash File (.txt)", type="txt")
    wordlist = st.text_input("Wordlist Path", "/usr/share/wordlists/rockyou.txt")
    
    if hash_file and st.button("🔥 Start Cracking"):
        with open("temp_hash.txt", "wb") as f:
            f.write(hash_file.getbuffer())
        
        st.info("Cracking in progress... check 'Show Status' for updates.")
        # Start John in the background
        subprocess.Popen(["john", "--wordlist=" + wordlist, "temp_hash.txt"])

    if st.button("📊 Show Cracking Status"):
        status = subprocess.run(["john", "--show", "temp_hash.txt"], capture_output=True, text=True)
        st.success("Cracked Passwords:")
        st.code(status.stdout if status.stdout else "No passwords cracked yet.")

# --- LIVE SNIFFER ---
st.divider()
if st.checkbox("📡 Show Active Connections"):
    connections = psutil.net_connections()
    df = pd.DataFrame([{"fd": c.fd, "family": c.family, "status": c.status} for c in connections])
    st.table(df.head(10))
