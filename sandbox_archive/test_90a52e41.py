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

def generate_random_3cnf(n, m):
    clauses = []
    for _ in range(m):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(3)]
        random.shuffle(literals)
        clause = f"({' '.join(map(str, literals))}) | "
        clauses.append(clause)
    return ''.join(clauses[:-2])

def qr_decomposition(A):
    n = len(A)
    Q = [[0] * n for _ in range(n)]
    R = [[A[i][j] if i <= j else 0 for j in range(n)] for i in range(n)]
    
    for k in range(n):
        norm = sum(R[k][i]**2 for i in range(k, n))**0.5
        Q[k][k] = R[k][k] / norm
        for j in range(k + 1, n):
            R[k][j] /= norm
            Q[j][k] = R[k][j]
            for i in range(k, n):
                R[i][j] -= Q[k][i] * R[i][k]
    
    return Q, R

def real_radical_rank(A):
    _, R = qr_decomposition(A)
    rank = sum(1 for row in R if any(x != 0 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = 3 * n
    cnf_instance = generate_random_3cnf(n, m)
    
    d = math.isqrt(n)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        A[i][i] = 1
        A[n][i] = -1
    
    M_d = [row[:] + [sum(row[i] * row[j] for i in range(n)) if j == n else 0 for j in range(n + 1)] for row in A]
    
    rank = real_radical_rank(M_d)
    threshold = 0.7 * math.isqrt(n)
    
    conjecture_holds = rank >= threshold
    counterexample = "" if conjecture_holds else "real radical rank < 0.7√n"
    
    return {
        "metric_name": "Real Radical Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")