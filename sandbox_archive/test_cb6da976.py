import random
import subprocess
from itertools import combinations
import json
from sympy import symbols, Poly, groebner

def generate_3cnf(n):
    variables = [symbols(f'x{i}') for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.choice(variables) | ~random.choice(variables)
        clauses.append(clause)
    return ' & '.join(map(str, clauses))

def compute_generator_count(formula):
    x = symbols('x')
    polys = [Poly(f.subs({y: x**2 for y in variables}), x) for f in formula.split(' & ')]
    gb = groebner(polys, x)
    return len(gb)

def compute_proof_size(formula):
    with open("temp.cnf", "w") as f:
        f.write(f"p cnf {len(formula.split(' & '))} 1\n")
        for clause in formula.split(' & '):
            f.write(f"{clause} 0\n")
    result = subprocess.run(["dpll", "-s", "temp.cnf"], capture_output=True, text=True)
    return len(result.stdout.strip().split('\n')) - 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        formula = generate_3cnf(n)
        generator_count = compute_generator_count(formula)
        proof_size = compute_proof_size(formula)
        
        results.append({
            "n": n,
            "formula": formula,
            "generator_count": generator_count,
            "proof_size": proof_size
        })
    
    metric_name = "asymptotic_growth_rate"
    counts = [r["generator_count"] for r in results]
    sizes = [r["proof_size"] for r in results]
    
    if len(counts) < 4:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    def growth_rate(lst):
        if not lst:
            return 0
        max_n = max(r["n"] for r in results)
        return (lst[-1] / lst[0]) ** (1 / (max_n - n_values[0]))
    
    count_growth = growth_rate(counts)
    size_growth = growth_rate(sizes)
    
    conjecture_holds = abs(count_growth - size_growth) < 1e-6
    counterexample = "" if conjecture_holds else "growth_rate_mismatch"
    
    return {
        "metric_name": metric_name,
        "metric_value": count_growth,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {json.dumps(trial_result)}")
        results.append(trial_result)
    
    total_count = sum(r["instances_tested"] for r in results)
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / total_count} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"growth_rate_mismatch\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE not_enough_data")