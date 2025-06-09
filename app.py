import streamlit as st
from cs import chatbot_response

st.set_page_config(page_title="고객센터 챗봇", layout="centered")

if 'chat_log' not in st.session_state:
    st.session_state['chat_log'] = []
if 'context' not in st.session_state:
    st.session_state['context'] = '메뉴선택'

st.title("📦 고객센터 챗봇")
st.markdown("문의하실 내용을 입력해 주세요. (예: '배송지 변경하고 싶어요')")

user_input = st.text_input("입력", key="user_input")

if user_input:
    response = chatbot_response(user_input)
    st.session_state.chat_log.append(("👤 고객", user_input))
    st.session_state.chat_log.append(("🤖 챗봇", response))
    st.session_state.user_input = ""  # 입력창 초기화

for speaker, message in st.session_state.chat_log:
    st.markdown(f"**{speaker}:** {message}")
