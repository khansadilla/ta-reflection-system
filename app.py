import streamlit as st
from fsm.fsm import fsm_step
from llm.model import llm

st.title("💬 Refleksi Bareng Dilla-Bot")
st.caption("Framework 5R (Bain et al., 2002) - TA Khansa Adilla")

# 1. Inisialisasi Session State (Tempat nyimpen variabel biar gak ilang)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"}]
    st.session_state.stage = "reporting_responding"
    st.session_state.stage_buffer = ""
    st.session_state.full_history = ""
    st.session_state.is_completed = False
    st.session_state.last_question = "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"

# 2. Tampilin Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle Input User
if not st.session_state.is_completed:
    if user_input := st.chat_input("Ceritain di sini ya..."):
        # Tambah input user ke UI & History
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.stage_buffer += "\n" + user_input.strip()
        st.session_state.full_history += "\nUSER: " + user_input.strip()

        # JALANKAN LOGIKA FSM (Sekarang pake 4 variabel!)
        with st.spinner("Lagi dengerin..."):
            # Update: Tangkap 'decision' juga dari fsm_step
            new_stage, next_question, new_buffer, decision = fsm_step(
                st.session_state.stage, 
                st.session_state.full_history, 
                llm, 
                st.session_state.stage_buffer
            )

        # Update Session State
        st.session_state.stage = new_stage
        st.session_state.stage_buffer = new_buffer
        st.session_state.full_history += "\nSYSTEM: " + next_question
        
        # Simpan pertanyaan baru buat ditampilin
        st.session_state.messages.append({"role": "assistant", "content": next_question})
        with st.chat_message("assistant"):
            st.markdown(next_question)

        # LOGIKA SELESAI (Sesuai script terminal kamu)
        if new_stage == "reconstructing" and decision == "advance":
            st.session_state.is_completed = True
            st.success("--- Refleksi selesai ---")
            st.write("Terima kasih sudah meluangkan waktu untuk merefleksikan hal ini hari ini.")
            st.balloons()