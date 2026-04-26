# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    A = gaussian_elimination(A)
    return sum(1 for row in A if any(row))

def mu(X, poset):
    if not X:
        return 1
    else:
        result = 0
        for x in poset[X[0]]:
            result -= mu(x, poset)
        return result

def zaslavsky_region_count(A_F):
    k = len(A_F)
    poset = {i: [] for i in range(k)}
    for X in range(1 << k):
        flat = True
        for i in range(k):
            if (X >> i) & 1:
                for j in range(i + 1, k):
                    if (X >> j) & 1 and A_F[i][j] == 0:
                        flat = False
                        break
                if not flat:
                    break
        if flat:
            poset[X].append(X ^ (1 << i))
    return sum(abs(mu(X, poset)) for X in range(1 << k))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    s = 2 * n
    d = 2
    
    # Generate CNF formula
    if seed % 3 == 0:  # MOD_3
        clauses = [[i for i in range(n) if (i // 3 + i % 3) % 3 == j] for j in range(3)]
    elif seed % 3 == 1:  # AND-of-MOD_2
        clauses = [[i for i in range(n) if (i // 2 + i % 2) % 2 == j] for j in range(2)]
    else:  # Random 3-CNF
        clauses = []
        for _ in range(random.randint(3 * n, 4 * n)):
            clause = random.sample(range(n), 3)
            clauses.append(clause)
    
    A_F = [[0] * n for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        pos_indices = [j for j in clause if (j // 2 + j % 2) % 2 == 1]
        neg_indices = [j for j in clause if (j // 2 + j % 2) % 2 == 0]
        A_F[i][pos_indices] = [1] * len(pos_indices)
        A_F[i][neg_indices] = [-1] * len(neg_indices)
    
    r_A_F = zaslavsky_region_count(A_F)
    log_r_A_F = math.log2(r_A_F)
    bound = 4 * d * (math.log2(s) + math.log2(n))
    
    conjecture_holds = log_r_A_F <= bound
    counterexample = "" if conjecture_holds else "small ACC^0 circuit but large r(A_F)"
    
    return {
        "metric_name": "log_r_A_F",
        "metric_value": log_r_A_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_A_F = sum(r["metric_value"] for r in results) / len(results)
    std_r_A_F = math.sqrt(sum((r["metric_value"] - mean_r_A_F) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_A_F} std={std_r_A_F} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"small ACC^0 circuit but large r(A_F)\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data to determine support or falsification")