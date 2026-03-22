import streamlit as st
import pandas as pd
import subprocess
import os

st.set_page_config(page_title="KALI OMNI-HUB", layout="wide")
st.title("💀 KALI OMNI-HUB: ALL-IN-ONE")

# --- SIDEBAR: OSINT & QUICK LOOKUP ---
st.sidebar.header("🔍 OSINT Quick-Tools")
ip_lookup = st.sidebar.text_input("IP/Domain Lookup")
if st.sidebar.button("Whois"):
    res = subprocess.run(["whois", ip_lookup], capture_output=True, text=True)
    st.sidebar.code(res.stdout)

# --- TABBED INTERFACE (The Kitchen Sink) ---
t1, t2, t3, t4 = st.tabs(["📡 Recon", "🌐 Web Audit", "🔓 Cracking", "💣 Exploits"])

with t1:
    st.header("Nmap Network Mapping")
    target = st.text_input("Target Range", "192.168.1.0/24")
    mode = st.selectbox("Scan Intensity", ["-sn (Ping Sweep)", "-sV (Service Scan)", "-A (Aggressive)"])
    if st.button("🚀 Execute Nmap"):
        with st.spinner("Scanning..."):
            res = subprocess.run(["nmap", mode, target], capture_output=True, text=True)
            st.code(res.stdout)

with t2:
    st.header("Nikto Web Vulnerability Scanner")
    web_target = st.text_input("URL (e.g., http://1.1.1.1)")
    if st.button("🔍 Audit Web Server"):
        with st.spinner("Running Nikto..."):
            res = subprocess.run(["nikto", "-h", web_target], capture_output=True, text=True)
            st.code(res.stdout)

with t3:
    st.header("John the Ripper")
    wordlist = st.text_input("Wordlist", "/usr/share/wordlists/rockyou.txt")
    if st.button("🔥 Start Cracker"):
        st.info("Cracking process spawned in background.")
        subprocess.Popen(["john", "--wordlist=" + wordlist, "temp_hash.txt"])

with t4:
    st.header("Searchsploit (Exploit-DB)")
    query = st.text_input("Search Vulnerability (e.g., 'Apache 2.4')")
    if st.button("🔎 Find Exploit"):
        res = subprocess.run(["searchsploit", query], capture_output=True, text=True)
        st.code(res.stdout)

st.divider()
st.caption("PHOENIX NODE | ENCRYPTED LINK ACTIVE")
