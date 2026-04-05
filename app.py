import streamlit as st
from fsm.fsm import fsm_step
from llm.model import llm  # Pastikan path-nya bener

# --- SETTING PAGE ---
st.set_page_config(page_title="Refleksi 5R Assistant", page_icon="💬")
st.title("💬 Refleksi Bareng Dilla-Bot")
st.caption("Framework 5R (Bain et al., 2002) - TA Khansa Adilla")

# --- 1. INISIALISASI VARIABEL (SESSION STATE) ---
if "messages" not in st.session_state:
    # Chat history buat ditampilin di layar
    st.session_state.messages = [{"role": "assistant", "content": "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"}]
    # Variabel logic kamu
    st.session_state.stage = "reporting_responding"
    st.session_state.stage_buffer = ""
    st.session_state.full_history = ""
    st.session_state.is_completed = False

# --- 2. TAMPILIN CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. INPUT USER ---
if not st.session_state.is_completed:
    if user_input := st.chat_input("Ceritain di sini ya..."):
        # Tambah ke UI
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Update buffer & history
        st.session_state.stage_buffer += "\n" + user_input.strip()
        st.session_state.full_history += "\nUSER: " + user_input.strip()

        # JALANKAN LOGIKA FSM (Judge & RAG Generator)
        with st.spinner("Lagi dengerin kamu..."):
            # Pastikan fsm_step kamu nerima parameter yang bener
            new_stage, next_question, new_buffer = fsm_step(
                st.session_state.stage, 
                st.session_state.full_history, 
                llm, 
                st.session_state.stage_buffer
            )

        # Update State
        st.session_state.stage = new_stage
        st.session_state.stage_buffer = new_buffer
        st.session_state.full_history += "\nSYSTEM: " + next_question
        
        # Simpan & Tampilkan respon Assistant
        st.session_state.messages.append({"role": "assistant", "content": next_question})
        with st.chat_message("assistant"):
            st.markdown(next_question)

        # Cek kalau sudah kelar
        if st.session_state.stage == "completed":
            st.session_state.is_completed = True
            st.success("Refleksi Selesai! Kamu hebat banget hari ini. ✨")
            st.balloons()