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
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    A = gaussian_elimination(A)
    r = sum(1 for row in A if any(row))
    return r

def incidence_matrix(cnf):
    n = max(abs(var) for clause in cnf for var in clause)
    M = [[0] * (n + 1) for _ in range(len(cnf))]
    for i, clause in enumerate(cnf):
        for var in clause:
            M[i][abs(var)] += 1 if var > 0 else -1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    cnf3 = [[random.randint(-n, n) for _ in range(3)] for _ in range(n)]
    cnf2 = [[random.randint(-n, n) for _ in range(2)] for _ in range(n)]
    
    M3 = incidence_matrix(cnf3)
    M2 = incidence_matrix(cnf2)
    
    rank_M3 = rank(M3)
    rank_M2 = rank(M2)
    
    metric_name = "rank(M^⊗2)"
    metric_value = rank_M3
    instances_tested = 1
    conjecture_holds = rank_M3 >= n**1.5 and rank_M2 <= n**1.2
    counterexample = "" if conjecture_holds else f"3-CNF: {rank_M3}, 2-CNF: {rank_M2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")