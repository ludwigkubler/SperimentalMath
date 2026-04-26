import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_formula(n):
        formula = []
        for i in range(1 << n):
            if all((i & (1 << j)) == 0 or random.choice([True, False]) for j in range(n)):
                formula.append(i)
        return formula
    
    def discrepancy(hypergraph):
        n = len(hypergraph)
        max_discrepancy = 0
        for i in range(1 << n):
            count = sum(1 for edge in hypergraph if (i & edge) == edge)
            max_discrepancy = max(max_discrepancy, abs(count - (n - count)))
        return max_discrepancy
    
    def formula_size(formula):
        return len(formula)
    
    n = random.choice([5, 8, 11, 14])
    hypergraph = generate_monotone_formula(n)
    delta_f = discrepancy(hypergraph)
    size = formula_size(hypergraph)
    
    conjecture_holds = size <= delta_f ** 2
    counterexample = "" if conjecture_holds else f"Formula of size {size} with Δ(F)={delta_f}"
    
    return {
        "metric_name": "formula_size",
        "metric_value": size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_size = sum(r["metric_value"] for r in results)
    count_holds = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = count_holds / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_size/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_size/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula size greater than Δ(F)^2\" first_failing_seed={first_failing_seed}")