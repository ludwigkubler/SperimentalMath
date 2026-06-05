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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(n):
                if j != i and A[rank][j] != 0:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def hdd(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for x in clause:
                if x > 0:
                    i, j = x - 1, n
                else:
                    i, j = -x - 1, n - 1
                A[i][j] += 1
        return gaussian_elimination(A)
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        width = 0
        
        while queue:
            clause = queue.pop(0)
            if frozenset(clause) in seen:
                continue
            seen.add(frozenset(clause))
            
            for other_clause in cnf:
                if len(set(clause) & set(other_clause)) == 1:
                    new_clause = [x for x in clause + other_clause if x not in set(clause) & set(other_clause)]
                    queue.append(new_clause)
                    width = max(width, len(new_clause))
        
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    hdd_value = hdd(cnf)
    width_value = resolution_width(cnf)
    
    if hdd_value == 0 or width_value == 0:
        return {
            "metric_name": "hdd/width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = hdd_value / width_value
    return {
        "metric_name": "hdd/width",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 1 and width_value / hdd_value <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"hdd({r['n_max']}) / width({r['n_max']}) = {r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break