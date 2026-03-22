#!/data/data/com.termux/files/usr/bin/bash
while true; do
  if ! pgrep -f "streamlit run badass_hub.py" > /dev/null; then
    echo "Hub offline. Restarting..."
    nohup streamlit run ~/badass-termux-os/badass_hub.py --server.port 8501 > /dev/null 2>&1 &
  fi
  sleep 60
done
