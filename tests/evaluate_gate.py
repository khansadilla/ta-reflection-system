import json
from collections import Counter

from fsm.fsm import llm_gate

def evaluate(dataset_path):
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

        strict_correct = 0
        relaxed_correct = 0
        total = 0

        confusion = Counter()

        for case in dataset:
            stage = case["stage"]
            stage_buffer = ""

            for turn in case["turns"]:

                text = turn["text"]

                stage_buffer +="\n"+ text

                pred = llm_gate(stage, stage_buffer)

                gold = turn["expected"]

                confusion[(gold, pred)]+=1

                if pred==gold:
                    strict_correct+=1
                
                if pred!=gold:
                    print("STAGE: ", stage)
                    print("TEXT: ", text)
                    print("GOLD: ", gold)
                    print("PRED: ", pred)
                    print("--------------------")
                acceptable = case.get("acceptable_label")

                if pred==gold or pred==acceptable:
                    relaxed_correct+=1
                
                total+=1

                if pred=="ADVANCE":
                    stage_buffer=""

        strict_acc = strict_correct/total
        relaxed_acc = relaxed_correct/total

        print("TOTAL:", total)
        print("STRICT ACCURACY:", round(strict_acc,3))
        print("RELAXED ACCURACY:", round(relaxed_acc,3))

        print("\nCONFUSION MATRIX")
        print("(gold -> predicted)\n")

        for (gold,pred), count in confusion.items():
            print(f"{gold}->{pred} : {count}")

if __name__ == "__main__":

    evaluate("tests/golden_set_gating.json")