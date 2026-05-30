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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_norm(cnf):
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        norm = 0
        for i in range(n):
            for j in range(i, n):
                count = sum(1 for clause in cnf if (i+1 in clause and j+1 not in clause) or (j+1 in clause and i+1 not in clause))
                norm += count * count
        return math.sqrt(norm)
    
    def resolution_length(cnf):
        stack = []
        while True:
            new_clause = None
            for i, clause1 in enumerate(cnf):
                for j, clause2 in enumerate(cnf):
                    if i == j: continue
                    common_lits = set(lit for lit in clause1 if -lit in clause2)
                    if len(common_lits) > 0:
                        new_clause = [lit for lit in clause1 if lit not in common_lits] + [lit for lit in clause2 if lit not in common_lits]
                        break
                if new_clause is not None: break
            if new_clause is None: break
            cnf.append(new_clause)
        return len(cnf) - m
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            m = random.randint(1, min(n * (n - 1) // 2, 100))  # Limit m to avoid excessive computation
            cnf = generate_cnf(m, n)
            norm = compute_norm(cnf)
            length = resolution_length(cnf)
            results.append({
                "metric_name": "norm",
                "metric_value": norm,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": True,
                "counterexample": ""
            })
    
    mean_norm = sum(result["metric_value"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["metric_value"] - mean_norm) ** 2 for result in results) / len(results))
    
    return {
        "seed": seed,
        "mean_norm": mean_norm,
        "std_norm": std_norm,
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(mean_norm * 0.95 <= norm <= mean_norm * 1.1 for norm in [result["metric_value"] for result in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_norm = sum(result["mean_norm"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["mean_norm"] - mean_norm) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"norm_exceeds_upper_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")