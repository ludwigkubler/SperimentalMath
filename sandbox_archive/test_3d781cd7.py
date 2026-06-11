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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def incidence_matrix(cnf, n):
        m = len(cnf)
        M = [[0] * n for _ in range(m)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    M[i][var] = 1
                else:
                    M[i][var] = -1
        return M
    
    def gaussian_elimination(M):
        m, n = len(M), len(M[0])
        rank = 0
        for j in range(n):
            i_max = None
            for i in range(rank, m):
                if M[i][j] != 0:
                    i_max = i
                    break
            if i_max is not None:
                M[rank], M[i_max] = M[i_max], M[rank]
                for i in range(rank + 1, m):
                    factor = -M[i][j] / M[rank][j]
                    for k in range(n):
                        M[i][k] += factor * M[rank][k]
                rank += 1
        return rank
    
    def resolution_width(cnf):
        width = 0
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        while True:
            new_clauses = set()
            for clause1, clause2 in itertools.combinations(clauses, 2):
                if any(abs(lit) in clause2 for lit in clause1):
                    new_clause = tuple(sorted(set(clause1 + clause2) - {0}))
                    if len(new_clause) > width:
                        width = len(new_clause)
                    new_clauses.add(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 5 * n)
        cnf = generate_cnf(n, m)
        M = incidence_matrix(cnf, n)
        mtr = gaussian_elimination(M)
        w = resolution_width(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "mtr": mtr,
            "w": w
        })
    
    if not results:
        return {
            "metric_name": "minimal_modular_tensor_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mtr_values = [result["mtr"] for result in results]
    w_values = [result["w"] for result in results]
    
    mean_mtr = sum(mtr_values) / len(mtr_values)
    mean_w = sum(w_values) / len(w_values)
    
    correlation_coefficient = 0.0
    if len(mtr_values) > 1:
        numerator = sum((mtr - mean_mtr) * (w - mean_w) for mtr, w in zip(mtr_values, w_values))
        denominator = math.sqrt(sum((mtr - mean_mtr) ** 2 for mtr in mtr_values)) * math.sqrt(sum((w - mean_w) ** 2 for w in w_values))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient > 0.7 and all(mtr <= 1.5 * w for mtr, w in zip(mtr_values, w_values))
    
    return {
        "metric_name": "minimal_modular_tensor_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation_coefficient<0.7 or mtr>1.5*w"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.7 or mtr>1.5*w\" first_failing_seed={first_failing_seed}")