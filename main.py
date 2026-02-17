from fsm.fsm import fsm_step
from llm.model import llm

stage = "reporting_responding"
question = "Kalau kamu memilih satu hal yang paling ingin kamu refleksikan hari ini, apa itu?"

while True:
    print("\n STAGE:",stage)
    print("Q:",question)

    user_text = input("YOU: ")

    stage, question = fsm_step(stage, user_text, llm)

    if stage=="reconstructing" :
        print("\n STAGE:",stage)
        print("Q:",question)

        user_text=input("YOU: ")
        print("\n--- Refleksi selesai ---")
        print("Terima kasih sudah meluangkan waktu untuk merefleksikan hal ini hari ini.")
        break
