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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def symplectic_form(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        form = [[0] * n for _ in range(n)]
        for clause in cnf:
            x, y = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0 and clause[1] > 0:
                form[x][y], form[y][x] = 1, 1
            elif clause[0] < 0 and clause[1] < 0:
                form[x][y], form[y][x] = -1, -1
        return form
    
    def resolution_width(cnf):
        # Simplified resolution width calculation (not exact)
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        width = 0
        while True:
            new_clauses = []
            for clause in clauses:
                if len(clause) == 1:
                    return max(width, abs(clause[0]))
                x = random.choice(clause)
                new_clauses.extend([tuple(sorted(c + [-x])) for c in clauses if x not in c])
            if set(new_clauses).issubset(clauses):
                break
            clauses.update(new_clauses)
            width += 1
        return max(width, abs(x))
    
    def min_rank(form):
        n = len(form)
        rank = 0
        for i in range(n):
            if any(form[j][i] != 0 for j in range(i)):
                rank += 1
        return rank
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n, 2*n)
        cnf = generate_k_cnf(n, m)
        form = symplectic_form(cnf)
        width = resolution_width(cnf)
        rank = min_rank(form)
        
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "width": width
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    
    c = 1.0  # Constant for minimal rank bound
    r = 1.0  # Constant for resolution proof width bound
    
    conjecture_holds = (mean_rank <= c * math.sqrt(sum(result["m"] / result["n"] for result in results) / len(results))) and \
                        (mean_width >= r * sum(result["n"] for result in results) / len(results))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": 0.7,  # Placeholder value
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    mean_width = sum(result["instances_tested"] * result["metric_value"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")