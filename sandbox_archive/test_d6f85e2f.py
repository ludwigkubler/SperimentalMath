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

def generate_k_cnf(n, q):
    if n <= 0 or q <= 1:
        return None
    clauses = []
    for _ in range(int(q * n / 2)):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(m)):
            continue
        pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
        matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
        rank += 1
        for j in range(m):
            if j == i:
                continue
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        q = random.randint(2, min(n, 10))
        clauses = generate_k_cnf(n, q)
        if not clauses:
            continue
        
        matrix = [[0] * (n + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                matrix[i][var - 1] = 1
            matrix[i][-1] = 1
        
        rank = matrix_rank(matrix)
        results.append({
            "n": n,
            "q": q,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank = min(result["rank"] for result in results)
    avg_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - avg_rank) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": min_rank >= 0.1 * n_values[0] ** (2/3) * q ** (1/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_too_low\" first_failing_seed={first_failing_seed}")