import sys
import json
from sympy import symbols, groebner, Poly, ZZ
from itertools import combinations

def run_trial(seed: int) -> dict:
    n = 14
    variables = [symbols(f'x{i}') for i in range(n)]
    
    # Generate a random 3-CNF formula with n variables and m clauses
    m = 2 * n
    cnf = []
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = variables[random.randint(0, n-1)]
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(~var)
        cnf.append(clause)
    
    # Convert CNF to polynomial ideal
    ideal = [Poly(' & '.join(map(str, clause)), *variables) for clause in cnf]
    ideal = groebner(ideal, *variables, domain=ZZ)
    
    # Compute the Hilbert function of the ideal
    hilbert_function = {}
    for i in range(n + 1):
        hilbert_function[i] = len([g for g in ideal if g.degree() == i])
    
    # Estimate communication complexity (simplified example)
    communication_complexity = n * m
    
    # Check if the Hilbert function's growth rate matches the communication complexity
    conjecture_holds = False
    counterexample = ""
    if hilbert_function[1] == communication_complexity:
        conjecture_holds = True
    else:
        counterexample = "Hilbert function does not match communication complexity"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {json.dumps(trial_result)}")
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")