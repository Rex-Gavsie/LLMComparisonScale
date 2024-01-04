"""
This is where I'll integrate the dilution code with the human eval tests and maybe with the other stuff

XXXX Idk if this works but hopefully it does
UPDATE IT DOES WORK WOOO we can generate samples jsonls, now to score those
"""
import concurrent.futures

from human_eval.human_eval.data import write_jsonl, read_problems
from ProofOfConcept import doWhatTomSevenSaidNormalCompletions, getStandardName



def generate_one_completion(prompt, exponentialDilution, dilutionProportion, iterations, maxTokens,task_id):
    """Idk if this will work as it might do stuff like talking after the code, 
    I hope temp being 0 will prevent that but idk"""
    print(f"Getting Response for task {task_id}")
    response = doWhatTomSevenSaidNormalCompletions(prompt, exponentialDilution, dilutionProportion, iterations, maxTokens)
    return response

def generate_one_sample(task_id, problems, exponentialDilution, dilutionProportion, callsPerTest, maxTokens):
    return dict(task_id=task_id,
        completion=generate_one_completion(
            problems[task_id]["prompt"],
            exponentialDilution,
            dilutionProportion,
            callsPerTest,
            maxTokens,
            task_id
        )
        )

def runHumanEvalTest35POCDilution(numSamplesPerTask, exponentialDilution, dilutionProportion, callsPerTest, maxTokens) -> None:
    """
    Run human eval at a given dilution of GPT-3.5-Turbo-Instruct 

    Parameters
    ----------
    numSamplesPerTask : int
        Number of samples each problem will have

    exponetialDilution : bool
        if true, will dilute the original model by 2 raised to dilutionProportion
    
    dilutionProportion : float
        Proportion of original model (0.7 means 70% original model), or, if exponentialDilution == true, 2^dilutionProportion
    
    callsPerTest : int
        how many times we ask the LLM for a response

    maxTokens : int
        max number of tokens generated per response
    
    """
    
    problems = read_problems()
    
    samples = [
        dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"], exponentialDilution, dilutionProportion, callsPerTest, maxTokens,task_id))
        for task_id in problems
        for _ in range(numSamplesPerTask)
    ]
    write_jsonl(f"{getStandardName('hEvalTest35', exponentialDilution, dilutionProportion, callsPerTest, maxTokens, numSamplesPerTask)}_Samples.jsonl", samples)

def testDilutionsOnHumanEval(testInterval,numPasses) -> None:
    for i in range(0,1+testInterval,testInterval):
        runHumanEvalTest35POCDilution(numPasses, False, i, 500, 1)

# runHumanEvalTest35POCDilution(10,False,1,1,500)

# runHumanEvalTest35POCDilution(2, False, 1, 10, 50)

def main(numSamplesPerTask, exponentialDilution, dilutionProportion, callsPerTest, maxTokens):

    problems = read_problems()

    with concurrent.futures.ProcessPoolExecutor() as executor:

        futures = [
            executor.submit(generate_one_sample, task_id, problems, exponentialDilution, dilutionProportion, callsPerTest, maxTokens)
            for task_id in problems
            for _ in range(numSamplesPerTask)
        ]

        samples = [future.result() for future in concurrent.futures.as_completed(futures)]

    write_jsonl(f"{getStandardName('hEvalTest35', exponentialDilution, dilutionProportion, callsPerTest, maxTokens, numSamplesPerTask)}_Samples.jsonl", samples)

if __name__ == "__main__":
    main(1,False,1,500,1)