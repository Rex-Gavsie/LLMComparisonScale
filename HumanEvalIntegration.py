"""
This is where I'll integrate the dilution code with the human eval tests and maybe with the other stuff

Idk, fuck it, we ball
"""


#literally just the example code
from human_eval.data import write_jsonl, read_problems
from ProofOfConcept import doWhatTomSevenSaidNormalCompletions

problems = read_problems()

num_samples_per_task = 200
samples = [
    dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
    for task_id in problems
    for _ in range(num_samples_per_task)
]
write_jsonl("samples.jsonl", samples)

def generate_one_completion(prompt):
    """Idk if this will work as it might do stuff like talking after the code, 
    I hope temp being 0 will prevent that but idk"""
    return doWhatTomSevenSaidNormalCompletions(prompt, False, 1, 10, 50) 
