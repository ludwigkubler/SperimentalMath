# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_3cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        clauses.append(clause)
    return clauses

def evaluate_formula(f_F, assignment):
    return all(any(f_F[var] == literal for var, literal in zip(clause, assignment)) for clause in f_F)

def compute_stab_1_3(f_F):
    n = len(next(iter(f_F)))
    rho = 1 / 3
    total = 0
    samples = 4000
    for _ in range(samples):
        x = [random.choice([-1, 1]) for _ in range(n)]
        y = [x[i] if random.random() < rho else -x[i] for i in range(n)]
        total += f_F[tuple(x)] * f_F[tuple(y)]
    return total / samples

def dpll(f_F, assignment, clauses):
    if not clauses:
        return 1
    var = next(iter(clauses[0]))
    for literal in [-1, 1]:
        new_assignment = assignment + [literal]
        new_clauses = [c for c in clauses if literal * c[var-1] != -1]
        if all(literal * f_F[tuple(a)] != -1 for a in new_assignment):
            result = dpll(f_F, new_assignment, new_clauses)
            if result > 0:
                return result
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    densities = [3.0, 4.26, 5.0]
    results = []
    
    for n in n_values:
        for alpha in densities:
            m = int(alpha * (2 ** n))
            for _ in range(50):
                clauses = generate_3cnf(n, m)
                f_F = {tuple([random.choice([-1, 1]) for _ in range(n)]): evaluate_formula(f_F, assignment) for assignment in itertools.product([-1, 1], repeat=n)}
                S_F = compute_stab_1_3(f_F)
                L_F = dpll(f_F, [], clauses)
                
                if not f_F.values():
                    continue
                
                expected_bound = (2 ** n) * S_F / (3 * m)
                if all(f_F.values()):
                    bound = (2 ** n) * (1 - 9 * S_F / m)
                else:
                    bound = (2 ** n) * S_F / (3 * m)
                
                if f_F.values():
                    if L_F < expected_bound:
                        results.append({"n": n, "alpha": alpha, "L_F": L_F, "S_F": S_F, "bound": bound, "conjecture_holds": False, "counterexample": "unsatisfiable"})
                else:
                    if L_F > bound:
                        results.append({"n": n, "alpha": alpha, "L_F": L_F, "S_F": S_F, "bound": bound, "conjecture_holds": False, "counterexample": "satisfiable"})
    
    metric_value = sum(result["L_F"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "L(F)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else results[0]["counterexample"]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")