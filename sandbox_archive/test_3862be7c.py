# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3xor_instance(n, alpha):
        m = int(alpha * n)
        clauses = []
        for _ in range(m):
            clause = [random.randint(0, 1) for _ in range(3)]
            while len(set(clause)) != 3:
                clause = [random.randint(0, 1) for _ in range(3)]
            clauses.append(clause)
        return clauses

    def count_satisfied_clauses(instance, assignment):
        return sum(all(assignment[i] == c for i, c in enumerate(clause)) for clause in instance)

    def projection(S_tau, i):
        proj = set()
        for x in S_tau:
            proj.add(tuple(x[:i] + x[i+1:]))
        return proj

    def loomis_whitney_defect(instance, alpha):
        n = len(instance[0])
        tau = 1 - 1 / (8 * alpha)
        S_tau = {tuple(assignment) for assignment in itertools.product([0, 1], repeat=n) if count_satisfied_clauses(instance, assignment) >= tau * len(instance)}
        
        total_log_proj_sizes = sum(math.log2(len(projection(S_tau, i))) for i in range(n))
        log_S_tau_size = math.log2(len(S_tau))
        return (total_log_proj_sizes / n - log_S_tau_size) / n

    n_values = [14, 16, 18, 20]
    alpha_values = [0.5, 0.7, 0.85, 0.918, 1.00, 1.10, 1.50]
    results = []

    for n in n_values:
        for alpha in alpha_values:
            instance = generate_3xor_instance(n, alpha)
            defect = loomis_whitney_defect(instance, alpha)
            results.append({
                "n": n,
                "alpha": alpha,
                "defect": defect
            })

    mean_defect = sum(result["defect"] for result in results) / len(results)
    std_dev_defect = math.sqrt(sum((result["defect"] - mean_defect) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Loomis-Whitney Defect",
        "metric_value": mean_defect,
        "instances_tested": len(results),
        "conjecture_holds": all(result["defect"] < 0.02 if result["alpha"] <= 0.85 else result["defect"] > 0.05 for result in results),
        "counterexample": "" if all(result["defect"] < 0.02 if result["alpha"] <= 0.85 else result["defect"] > 0.05 for result in results) else f"Defect out of bounds at alpha={result['alpha']}, defect={result['defect']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_defect = sum(result["metric_value"] for result in results) / len(results)
    std_dev_defect = math.sqrt(sum((result["metric_value"] - mean_defect) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_defect} std={std_dev_defect} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Defect out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")