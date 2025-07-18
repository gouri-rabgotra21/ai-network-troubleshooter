import streamlit as st
from ping3 import ping
import io
import datetime

# Simulated ping results
simulated_pings = {
    "192.168.1.1": "Request timed out",
    "192.168.1.2": "Success",
    "192.168.1.10": "TTL expired",
    "192.168.1.11": "Success"
}

# Suggestions for statuses
suggestions = {
    "Success": "✅ Device is reachable.",
    "TTL expired": "⚠️ Routing issue. Check intermediate devices.",
    "Request timed out": "❌ Check device power, cable, or config."
}

# AI assistant dummy logic
def get_ai_response(user_input):
    user_input = user_input.lower()
    if "router" in user_input:
        return "Check if the router is powered on and interfaces are up."
    elif "switch" in user_input:
        return "Ensure switch ports are active and cables connected."
    elif "pc1" in user_input:
        return "PC1 may have wrong IP or not connected. Check cable."
    elif "pc2" in user_input:
        return "PC2 might be off or misconfigured."
    return "Please check connections and IP settings."

st.set_page_config(page_title="AI Network Troubleshooter", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
html, body {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}
.title {
    font-size: 2.6rem;
    text-align: center;
    color: #8b5e3c;
    margin-bottom: 1.5rem;
}
.device-box {
    background: #2e2e2e;
    padding: 1.2rem;
    margin-bottom: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: transform 0.3s ease;
}
.device-box:hover {
    transform: scale(1.02);
    background: #3a3a3a;
}
.status {
    font-weight: bold;
}
.chatbot {
    background-color: #2b2b2b;
    border-radius: 10px;
    padding: 1rem;
    margin-top: 3rem;
}
.chatbot-header {
    font-weight: bold;
    font-size: 1.3rem;
    color: #ccc;
    margin-bottom: 0.5rem;
}
.user-msg {
    color: #91d1f0;
}
.bot-msg {
    color: #f0d191;
}
.footer {
    margin-top: 4rem;
    font-size: 0.9rem;
    text-align: center;
    color: #888;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<div class='title'>🧠 AI-Driven Network Troubleshooter</div>", unsafe_allow_html=True)
st.subheader("📶 Ping Device Status")

# --- Report Area ---
report_data = ""
for ip, status in simulated_pings.items():
    suggestion = suggestions.get(status, "")
    color = "lightgreen" if status == "Success" else "orange" if status == "TTL expired" else "red"

    style = "color:#8b5e3c" if ip == "192.168.1.1" else ""
    html_box = f"""
        <div class='device-box'>
            <b>Device ({ip}):</b> <span class='status' style='color:{color}'>{status}</span><br/>
            <span style='{style}'><i>{suggestion}</i></span>
        </div>
    """
    st.markdown(html_box, unsafe_allow_html=True)
    report_data += f"Device {ip}: {status} - {suggestion}\n"

# --- Upload .pkt file ---
st.markdown("### 📤 Upload Cisco .pkt File (Optional)")
pkt_file = st.file_uploader("Upload a Packet Tracer (.pkt) file", type=["pkt"])
if pkt_file:
    st.success(f"✅ '{pkt_file.name}' uploaded. You can now simulate this in Cisco Packet Tracer.")
    st.info("Note: This app doesn't parse .pkt file content. Use it to document your design.")

# --- Download Report Button ---
st.markdown("### 📥 Download Network Report")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"network_report_{timestamp}.txt"
st.download_button(
    label="⬇️ Download Troubleshooting Report",
    data=report_data,
    file_name=filename,
    mime="text/plain"
)

# --- Chatbot Section ---
st.markdown("<div class='chatbot'>", unsafe_allow_html=True)
st.markdown("<div class='chatbot-header'>🤖 Ask AI Assistant</div>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for q, a in st.session_state.chat_history:
    st.markdown(f"<div class='user-msg'><b>You:</b> {q}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-msg'><b>Bot:</b> {a}</div>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your troubleshooting question:")
    submitted = st.form_submit_button("Send")
    if submitted and user_input:
        response = get_ai_response(user_input)
        st.session_state.chat_history.append((user_input, response))
        st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div class='footer'>Project by <b>Gouri Rabgotra</b> © 2025</div>", unsafe_allow_html=True)
