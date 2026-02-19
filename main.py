from fsm.fsm import fsm_step
from llm.model import llm

stage = "reporting_responding"
stage_buffer=""
full_history=""
question = "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"

while True:
    print("\n STAGE:",stage)
    print("Q:",question)

    user_text = input("YOU: ")

    full_history+="\nUSER:"+user_text.strip()

    stage, question, stage_buffer = fsm_step(stage, user_text, llm, stage_buffer)

    full_history+="\nSYSTEM: " + question

    if stage=="reconstructing" :
        print("\n--- Refleksi selesai ---")
        print("Terima kasih sudah meluangkan waktu untuk merefleksikan hal ini hari ini.")
        break
