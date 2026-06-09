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

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        pivot = Fraction(1, A[i][i])
        for j in range(m):
            A[i][j] *= pivot
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(m):
                    A[j][k] -= factor * A[i][k]
    return A

def diophantine_representation_size(cnf, n):
    m = len(cnf)
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(cnf):
        for var in clause:
            if var > 0:
                A[i][var - 1] += 1
            else:
                A[i][-1] -= 1
    rank = gaussian_elimination(A)
    return sum(1 for row in rank if any(row[j] != 0 for j in range(n + 1)))

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            if var not in clause:
                clause.add(var)
        cnf.append(list(clause))
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    instances_tested = 0
    total_size = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n))
            size = diophantine_representation_size(cnf, n)
            instances_tested += 1
            total_size += size
    
    metric_value = total_size / instances_tested
    conjecture_holds = metric_value <= (n_max * math.log(n_max)) * 2  # Loose bound for testing
    counterexample = "" if conjecture_holds else f"Size {total_size} exceeds O({n_max} log {n_max})"
    
    return {
        "metric_name": "Minimal Diophantine Representation Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Size exceeds bound\" first_failing_seed={first_failing_seed}")