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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    A = gaussian_elimination(A)
    r = sum(1 for row in A if any(row))
    return r

def generate_cnf(n, m, clauses_per_var=3):
    variables = list(range(1, n + 1))
    cnf = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * random.choice(variables) for _ in range(clauses_per_var)]
        cnf.append(clause)
    return cnf

def incidence_matrix(cnf):
    n = max(abs(x) for x in cnf[0])
    m = len(cnf)
    M = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(cnf):
        for var in clause:
            M[i][abs(var)] += 1 if var > 0 else -1
    return M

def symmetric_square(M):
    n = len(M)
    M2 = [[sum(M[i][k] * M[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return M2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m3 = 15 * n
    m2 = 7 * n
    
    cnf3 = generate_cnf(n, m3)
    cnf2 = generate_cnf(n, m2)
    
    M3 = incidence_matrix(cnf3)
    M2 = incidence_matrix(cnf2)
    
    rank_M3_sq = rank(symmetric_square(M3))
    rank_M2_sq = rank(symmetric_square(M2))
    
    metric_name = "rank"
    metric_value = rank_M3_sq / n**1.5 - rank_M2_sq / n**1.2
    instances_tested = 1
    conjecture_holds = abs(metric_value) > 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")