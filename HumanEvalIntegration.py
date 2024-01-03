"""
This is where I'll integrate the dilution code with the human eval tests and maybe with the other stuff

XXXX Idk if this works but hopefully it does
UPDATE IT DOES WORK WOOO we can generate samples jsonls, now to score those
"""
from human_eval.human_eval.data import write_jsonl, read_problems
from ProofOfConcept import doWhatTomSevenSaidNormalCompletions, getStandardName



def generate_one_completion(prompt, exponentialDilution, dilutionProportion, iterations, maxTokens):
    """Idk if this will work as it might do stuff like talking after the code, 
    I hope temp being 0 will prevent that but idk"""
    print("Getting Response...")
    response = doWhatTomSevenSaidNormalCompletions(prompt, exponentialDilution, dilutionProportion, iterations, maxTokens)
    return response


def runHumanEvalTest35POCDilution(numSamplesPerTask, exponentialDilution, dilutionProportion, iterations, maxTokens) -> None:
    """
    
    """
    
    problems = read_problems()
    
    samples = [
        dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"], exponentialDilution, dilutionProportion, iterations, maxTokens))
        for task_id in problems
        for _ in range(numSamplesPerTask)
    ]
    write_jsonl(f"{getStandardName('hEvalTest35', exponentialDilution, dilutionProportion, iterations, maxTokens, numSamplesPerTask)}_Samples.jsonl", samples)

runHumanEvalTest35POCDilution(10,False,1,10,50)

# runHumanEvalTest35POCDilution(2, False, 1, 10, 50)