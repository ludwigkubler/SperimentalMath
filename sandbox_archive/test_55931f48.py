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
    
    def generate_kcnf(n, k):
        literals = [f"v{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(k):
            clause = random.sample(literals + [-l for l in literals], 3)
            clauses.append(clause)
        return clauses
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if i == j:
                    continue
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def resolution_width(clauses):
        queue = clauses[:]
        while queue:
            clause1 = queue.pop()
            for clause2 in clauses:
                if set(clause1) & set(clause2):
                    new_clause = [l for l in clause1 + clause2 if l not in (set(clause1) & set(clause2))]
                    if len(new_clause) == 0:
                        return 1
                    queue.append(new_clause)
        return float('inf')
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(7):  # Aim for at least 30 instances per seed
            k = random.randint(n // 2, n)
            cnf = generate_kcnf(n, k)
            matrix = [[Fraction(1 if l == var else -1 if l == -var else 0) for var in range(1, n+1)] for clause in cnf]
            r_F = matrix_rank(matrix)
            t_star = resolution_width(cnf)
            
            if t_star <= 0:
                continue
            
            log_t_star = math.log2(t_star)
            phi_n = Fraction(1, 2) * math.log2(n)  # Placeholder for actual upper bound function
            
            results.append({
                "n": n,
                "k": k,
                "r_F": r_F,
                "t_star": t_star,
                "log_t_star": log_t_star,
                "phi_n": phi_n
            })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_r_F = sum(result["r_F"] for result in results) / len(results)
    mean_log_t_star = sum(result["log_t_star"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["log_t_star"] <= result["r_F"] and result["r_F"] <= result["phi_n"]) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_r_F,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Failed for n={results[0]['n']}, k={results[0]['k']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_r_F = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_F} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Failed for n={results[0]['n']}, k={results[0]['k']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")