import streamlit as st
import pandas as pd
import subprocess
import psutil

st.set_page_config(page_title="KALI GUI: PHOENIX", layout="wide")
st.title("🛡️ KALI RECON DASHBOARD")

# --- SIDEBAR: SYSTEM VITALS ---
st.sidebar.header("📡 Node Status")
st.sidebar.metric("CPU", f"{psutil.cpu_percent()}%")
st.sidebar.metric("RAM", f"{psutil.virtual_memory().percent}%")

# --- MAIN: NETWORK RECON ---
st.header("🔍 Network Discovery")
target = st.text_input("Target Range (e.g., 192.168.1.0/24)", "127.0.0.1")

if st.button("🚀 Run Nmap Scan"):
    with st.spinner("Scanning..."):
        # Run a quick service discovery scan
        cmd = ["nmap", "-sV", "-T4", target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        st.subheader("Scan Results")
        st.code(result.stdout)

# --- SNIFFER TAB ---
st.divider()
if st.checkbox("📡 Show Active Connections"):
    connections = psutil.net_connections()
    df = pd.DataFrame([{"fd": c.fd, "family": c.family, "type": c.type, "status": c.status} for c in connections])
    st.table(df.head(10))
