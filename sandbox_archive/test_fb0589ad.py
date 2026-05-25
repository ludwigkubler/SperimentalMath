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

def generate_kcnf(n, k):
    literals = list(range(1, n + 1))
    cnf = []
    for _ in range(k):
        clause = random.sample(literals + [-l for l in literals], 3)
        cnf.append(clause)
    return cnf

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if all(matrix[i][j] == 0 for j in range(n)):
            continue
        pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
        for j in range(i + 1, m):
            factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
        rank += 1
    return rank

def resolution_width(cnf):
    clauses = cnf[:]
    width = len(clauses)
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                for l in range(1, len(clauses[i])):
                    if -clauses[i][l] in clauses[j]:
                        new_clause = [x for x in clauses[i][:l-1] + clauses[i][l+1:] if x not in clauses[j]]
                        new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses.extend(new_clauses)
        width = max(width, len(clauses))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_kcnf(n, k=5 * n)
        t_star = resolution_width(cnf)
        if t_star == 0:
            continue
        r_F = matrix_rank(cnf)
        if r_F == 0:
            continue
        
        results.append({
            "n": n,
            "t_star": t_star,
            "r_F": r_F
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    total_r_F = sum(result["r_F"] for result in results)
    avg_t_star = sum(math.log2(result["t_star"]) for result in results) / len(results)
    avg_r_F = total_r_F / len(results)
    c = 1.0  # Absolute constant
    phi_n = c * math.log2(n_values[-1])
    
    conjecture_holds = all(avg_t_star <= avg_r_F and avg_r_F <= phi_n for _ in range(len(results)))
    counterexample = "" if conjecture_holds else "No valid instances found"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": avg_r_F,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"No valid instances found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No valid instances found")