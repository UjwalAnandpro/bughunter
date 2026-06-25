import streamlit as st

from ssh_client import SSHClient
from lmstudio import LMStudio
from history import History

st.set_page_config(page_title="CyberSecurity AI", page_icon="🛡️", layout="wide")

ai = LMStudio()
history = History()

st.title("🛡️ CyberSecurity AI")

st.sidebar.title("Settings")
host = st.sidebar.text_input("Kali IP", value="192.168.137.190")
username = st.sidebar.text_input("Username", value="ujwal")
key = st.sidebar.text_input("SSH Key", value=r"C:\Users\ujwal\.ssh\id_ed25519")

st.sidebar.divider()

if ai.check_server():
    st.sidebar.success("🟢 LM Studio Online")
else:
    st.sidebar.error("🔴 LM Studio Offline")

st.sidebar.divider()
st.sidebar.subheader("📜 History")

rows = history.get_all()

if not rows:
    st.sidebar.info("No History")
else:
    for row in rows[:10]:
        st.sidebar.caption(row[1])
        st.sidebar.write(row[2])

if st.sidebar.button("🗑 Clear History"):
    history.delete_all()
    st.rerun()

prompt = st.text_area("Prompt", placeholder="Example:\nshow current user")

if st.button("🚀 Run"):
    if not prompt.strip():
        st.warning("Enter a prompt.")
        st.stop()

    with st.spinner("Generating command..."):
        command = ai.generate_command(prompt)

    st.subheader("💻 AI Command")
    st.code(command, language="bash")

    ssh = SSHClient(host, username, key)
    ok, msg = ssh.connect()

    if not ok:
        st.error(msg)
        st.stop()

    st.sidebar.success("🟢 SSH Connected")

    with st.spinner("Executing command..."):
        ok, output = ssh.run_command(command)

    ssh.disconnect()

    st.subheader("📟 Terminal Output")
    st.code(output)

    with st.spinner("Analyzing output..."):
        analysis = ai.analyze_output(command, output)

    history.save(prompt, command, output, analysis)

    st.subheader("🧠 AI Analysis")
    st.write(analysis)
