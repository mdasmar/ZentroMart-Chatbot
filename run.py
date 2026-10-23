import streamlit as st
from src.retreiver import respond
from src.voice import STT,TTS
from src.rec_play import start_recording, stop_recording, play_audio

st.set_page_config(
    page_title="ZentroMart Assistant",
    page_icon="🛍️",
    layout="centered"
)

st.markdown(
    "<h1 style='text-align: center;'>ZentroMart Assistant</h1>",
    unsafe_allow_html=True
)

st.divider()

if "msg_history" not in st.session_state:
    st.session_state["msg_history"]=[]

if "recording" not in st.session_state:
    st.session_state.recording=False

for msg in st.session_state["msg_history"]:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])

question = st.chat_input(
    "Type your question here...",
    disabled=st.session_state.recording
)

if question:
    st.session_state["msg_history"].append({"role": "user","content": question})

    with st.chat_message("user"):
        st.text(question)

    with st.spinner("thinking..."):
        res=TTS(question)
    
    with st.chat_message('assistant'):
        st.write(res)
        play_audio("sample_reply/reply.wav")

    st.session_state["msg_history"].append({"role": "assistant","content": res})
        
st.markdown("""
<style>
div.stButton > button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

label = "⏹️ Stop Recording" if st.session_state.recording else "🎤 Voice Assist"

if st.button(label, use_container_width=True):

    if not st.session_state.recording:
        start_recording()
        st.session_state.recording = True

    else:
        stop_recording()
        st.session_state.recording = False

        hear=STT("sample_voice/ques.wav")

        with st.chat_message("user"):
            st.write(hear)

        st.session_state["msg_history"].append({"role": "user", "content": hear})

        with st.spinner("thinking..."):
            rep=TTS(hear)

        with st.chat_message("assistant"):
            st.write(rep)
            play_audio("sample_reply/reply.wav")

        st.session_state["msg_history"].append({"role": "assistant", "content": rep})

    st.rerun()