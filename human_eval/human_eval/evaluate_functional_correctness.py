import fire
import sys

from data import HUMAN_EVAL
from evaluation import evaluate_functional_correctness


def entry_point(
    sample_file: str,
    k: str = "1,10,100",
    n_workers: int = 4,
    timeout: float = 3.0,
    problem_file: str = HUMAN_EVAL,
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"
    """
    k = list(map(int, k.split(",")))
    results = evaluate_functional_correctness(sample_file, k, n_workers, timeout, problem_file)
    print(results)


if __name__ == '__main__':
    # fire.Fire(entry_point)
    
    results = evaluate_functional_correctness("C:\\Users\\Rex\\Documents\\VS Code General Projects\\LLMComparisonScale\\hEvalTest35_noExp_1dPro_500CPT_1Tkns_1SPT_Samples.jsonl")
    print(results)


# sys.exit(main())

# results = evaluate_functional_correctness("C:\\Users\\Rex\\Documents\\VS Code General Projects\\LLMComparisonScale\\samples.jsonl")
# print(results)