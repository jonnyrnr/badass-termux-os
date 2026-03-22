import streamlit as st
import psutil, os
from datetime import datetime

st.set_page_config(page_title="NEON COMMAND", layout="wide")
st.title("⚡ NEON COMMAND: PHOENIX NODE")

# --- WORK LOG ---
st.header("📋 Stagehand Work Log")
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 CLOCK IN"):
        with open("work_log.txt", "a") as f:
            f.write(f"IN:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        st.success("Clocked In!")
with c2:
    if st.button("🛑 CLOCK OUT"):
        with open("work_log.txt", "a") as f:
            f.write(f"OUT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        st.warning("Clocked Out!")

if st.checkbox("View History"):
    if os.path.exists("work_log.txt"):
        st.text(open("work_log.txt").read())

# --- STATUS ---
st.divider()
st.sidebar.header("🛠️ STATUS")
bat = psutil.sensors_battery()
st.sidebar.write(f"Battery: {bat.percentage}%" if bat else "On AC")
if st.sidebar.button("🔦 TOGGLE LIGHT"):
    os.system("termux-torch on")
