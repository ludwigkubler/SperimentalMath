import sys
from itertools import product
import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def all_3cnfs(n, max_clauses):
        clauses = []
        for _ in range(max_clauses):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(tuple(sorted(clause)))
        return set(frozenset(c) for c in clauses)
    
    def f_phi(phi, assignment):
        return any(all(phi[i][abs(j)-1] == j for j in clause) for clause in phi)
    
    def average_sensitivity(phi, n):
        total = 0
        for assignment in product([-1, 1], repeat=n):
            sensitivity = sum(1 for i in range(n) if f_phi(phi, tuple(assignment[:i] + (j,) + assignment[i+1:] for j in [-1, 1])) != f_phi(phi, assignment))
            total += sensitivity
        return total / (2**n * n)
    
    def resolution_width(phi):
        def dpll(phi, assignment, path, width):
            if not phi:
                return True
            var = next((v for v in range(1, len(phi[0])+1) if v not in assignment), None)
            if var is None:
                return False
            pos_var = (var, 1)
            neg_var = (-var, -1)
            if pos_var not in assignment and dpll(phi, assignment + [pos_var], path + [pos_var], width):
                return True
            if neg_var not in assignment and dpll(phi, assignment + [neg_var], path + [neg_var], width):
                return True
            return False
        
        max_width = 0
        for assignment in product([-1, 1], repeat=n):
            if f_phi(phi, assignment):
                path = []
                if not dpll(phi, assignment, path, 0):
                    return -1
                max_width = max(max_width, len(path))
        return max_width
    
    n_values = [5, 8, 11, 14]
    results = []
    
    for n in n_values:
        phi = all_3cnfs(n, 10)
        as_value = average_sensitivity(phi, n)
        w_phi = resolution_width(phi)
        
        if w_phi == -1 or w_phi < 0.5 * (as_value ** 0.5):
            return {
                "metric_name": "average_sensitivity",
                "metric_value": as_value,
                "instances_tested": len(phi),
                "conjecture_holds": False,
                "counterexample": f"Counterexample for n={n}, w(φ)={w_phi}, as(f_φ)={as_value}"
            }
        
        results.append(w_phi)
    
    return {
        "metric_name": "average_sensitivity",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(phi),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds if result["conjecture_holds"]]
    support_fraction = len(results) / len(seeds)
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")