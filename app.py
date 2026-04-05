import streamlit as st
from fsm.fsm import fsm_step
from llm.model import llm

# --- SETTING PAGE ---
st.set_page_config(page_title="Refleksi Bareng Dilla-Bot", page_icon="💬")

# --- 1. SIDEBAR (Developer Mode & Reset) ---
with st.sidebar:
    st.title("🛠️ Developer Tools")
    # Tombol Reset
    if st.button("Reset Percakapan", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.divider()
    # Info Stage saat ini
    current_s = st.session_state.get('stage', 'reporting_responding')
    st.write(f"📍 **Current Stage:**\n`{current_s}`")
    
    # Progress Bar 5R
    progress_map = {"reporting_responding": 20, "relating": 40, "reasoning": 60, "reconstructing": 80, "completed": 100}
    st.progress(progress_map.get(current_s, 0))

st.title("💬 Refleksi Bareng Dilla-Bot")
st.caption("Framework 5R (Bain et al., 2002) - TA Khansa Adilla")

# 2. Inisialisasi Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"}]
    st.session_state.stage = "reporting_responding"
    st.session_state.stage_buffer = ""
    st.session_state.full_history = ""
    st.session_state.is_completed = False

# 3. Tampilin Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Input User
if not st.session_state.is_completed:
    if user_input := st.chat_input("Ceritain di sini ya..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.stage_buffer += "\n" + user_input.strip()
        st.session_state.full_history += "\nUSER: " + user_input.strip()

        with st.spinner("Lagi dengerin..."):
            new_stage, next_question, new_buffer, decision = fsm_step(
                st.session_state.stage, 
                st.session_state.full_history, 
                llm, 
                st.session_state.stage_buffer
            )

        # --- TAMBAHAN BARU: NOTIFIKASI TOAST ---
        if new_stage != st.session_state.stage:
            notif_messages = {
                "relating": "✨ Wah, kamu mulai nemu polanya nih...",
                "reasoning": "🧠 Analisis kamu makin dalem, mantap!",
                "reconstructing": "🚀 Sip! Saatnya kita susun rencana nyata.",
                "completed": "✅ Refleksi selesai! Bangga banget sama kamu!"
            }
            pesan = notif_messages.get(new_stage, "📈 Progres refleksi meningkat!")
            st.toast(pesan, icon="🔔")

        # Update Session State
        st.session_state.stage = new_stage
        st.session_state.stage_buffer = new_buffer
        st.session_state.full_history += "\nSYSTEM: " + next_question
        
        st.session_state.messages.append({"role": "assistant", "content": next_question})
        with st.chat_message("assistant"):
            st.markdown(next_question)

        if new_stage == "reconstructing" and decision == "advance":
            st.session_state.is_completed = True
            st.success("--- Refleksi selesai ---")
            st.write("Terima kasih sudah meluangkan waktu untuk merefleksikan hal ini hari ini.")
            st.balloons()