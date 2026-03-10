from fsm.fsm import fsm_step
from llm.model import llm

def run_full_session(user_inputs):
    stage = "reporting_responding"
    stage_buffer = ""
    turns = 0

    for text in user_inputs:
        stage, question, stage_buffer = fsm_step(stage, text, llm, stage_buffer)
        turns += 1

        if stage == "reconstructing":
            return True, turns

    return False, turns


def run_baseline():
    sessions = [
        [
            "kemarin aku presentasi dan kecewa",
            "ini mirip kayak dulu aku takut dinilai gagal",
            "mungkin aku terlalu butuh validasi",
            "mulai minggu depan aku mau latihan presentasi tiap minggu"
        ],
        [
            "aku kesel aja sih",
            "ya gitu deh",
            "nggak tau kenapa",
        ],
    ]

    completed = 0
    total_turns = 0

    for s in sessions:
        done, turns = run_full_session(s)
        if done:
            completed += 1
        total_turns += turns

    print("\n===== END-TO-END BASELINE =====")
    print("Completion Rate:", completed / len(sessions))
    print("Average Turns:", total_turns / len(sessions))
    print("================================\n")


if __name__ == "__main__":
    run_baseline()