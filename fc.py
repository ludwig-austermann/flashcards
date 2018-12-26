#call with tex-file res-file file-opt general-opt
import sys, json, re
import flashcard as fcl

theorems = [fcl.Texobject("Aufgabe", r"\begin{task}", r"\end{task}")]
counter = fcl.Counter([0], [r"\begin{task}"], lambda x: x[0]%2)

with open(sys.argv[1], "r") as f:
    now_t = None; mode = 0; temp = ""; res = []
    for line in f.readlines():
        counter.count_with(line)
        if mode:
            if now_t.keyword[1] in line:
                res.append(fcl.Content(now_t, temp, "Dont know", str(counter)))
                temp = ""; mode = 0
            else:
                temp += line
        else:
            for theo in theorems:
                if theo.keyword[0] in line:
                    mode = 1; now_t = theo
    with open("data.json", "w") as wf:
        json.dump([card.json() for card in res], wf)

print("Done!")