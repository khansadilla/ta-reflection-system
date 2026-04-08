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

if "stage" not in st.session_state:
    st.session_state.stage = "reporting_responding"

if "stage_buffer" not in st.session_state:
    st.session_state.stage_buffer = ""

if "full_history" not in st.session_state:
    st.session_state.full_history = ""

if "is_completed" not in st.session_state:
    st.session_state.is_completed = False

if "last_question" not in st.session_state:
    # Isi dengan pertanyaan pertama biar Judge punya konteks awal
    st.session_state.last_question = "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"

if "previous_stage" not in st.session_state:
    st.session_state.previous_stage = None

# 3. Tampilin Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Input User
if not st.session_state.is_completed:
    if user_input := st.chat_input("Ceritain di sini ya..."):
        st.session_state.last_user_input = user_input
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
                st.session_state.stage_buffer,
                st.session_state.last_question,
                st.session_state.last_user_input
            )

        st.session_state.last_question = next_question

        # --- HANDLE STAGE CHANGE ---
        prev_stage = st.session_state.previous_stage
        curr_stage = new_stage

        stage_changed = (curr_stage != prev_stage) and (prev_stage is not None)

        st.session_state.stage = curr_stage

        # --- NOTIFIKASI TOAST ---
        if stage_changed:
            notif_messages = {
                "relating": "✨ Wah, kamu mulai nemu polanya nih...",
                "reasoning": "🧠 Analisis kamu makin dalem, mantap!",
                "reconstructing": "🚀 Sip! Saatnya kita susun rencana nyata.",
                "completed": "✅ Refleksi selesai! Bangga banget sama kamu!"
            }
            pesan = notif_messages.get(curr_stage, "📈 Progres refleksi meningkat!")
            st.toast(pesan, icon="🔔")

        st.session_state.previous_stage = curr_stage
        st.session_state.stage = curr_stage

        st.session_state.stage_buffer = new_buffer
        st.session_state.full_history += "\nSYSTEM: " + next_question
        
        st.session_state.messages.append({"role": "assistant", "content": next_question})
        with st.chat_message("assistant"):
            st.markdown(next_question)

        # --- HANDLE COMPLETION ---
        if new_stage == "completed":
            st.session_state.is_completed = True

            summary = llm.generate_summary(st.session_state.full_history)
            st.subheader("🪞 Ringkasan Refleksi Kamu")
            st.write(summary)
            st.balloons()