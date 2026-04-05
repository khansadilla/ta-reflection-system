from fsm.fsm import fsm_step
from llm.model import llm
import sys


stage = "reporting_responding"
stage_buffer=""
full_history=""
question = "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"

try:
    while True:
        print("\n STAGE:",stage)
        print("Q:",question)

        user_text = input("YOU: ")
        stage_buffer+="\n"+user_text.strip()

        full_history+="\nUSER:"+user_text.strip()

        stage, question, stage_buffer, decision = fsm_step(stage, full_history, llm, stage_buffer)

        full_history+="\nSYSTEM: " + question

        if stage=="reconstructing" and decision=="advance" :
            print("\n--- Refleksi selesai ---")
            print("Terima kasih sudah meluangkan waktu untuk merefleksikan hal ini hari ini.")
            break
except KeyboardInterrupt:
    print("\nExiting cleanly...")
    sys.exit(0)
