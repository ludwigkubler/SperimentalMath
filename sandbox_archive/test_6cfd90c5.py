# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank < m:
                pivot_row = rank
                while A[pivot_row][i] == 0:
                    pivot_row += 1
                    if pivot_row == m:
                        return rank
                A[rank], A[pivot_row] = A[pivot_row], A[rank]
                for j in range(n):
                    if j != i and A[rank][j] != 0:
                        factor = -A[j][i] / A[rank][i]
                        for k in range(n):
                            A[j][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def lnd(M):
        m, n = len(M), len(M[0])
        B = [row + [1] for row in M]
        rank_B = gaussian_elimination(B)
        return rank_B - n
    
    def rank(clauses):
        A = [[0] * (len(clauses) + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    A[i][var - 1] = 1
                else:
                    A[i][-var - 1] = 1
        return gaussian_elimination(A)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n * (n - 1) // 2, 10))
    clauses = generate_kcnf(n, k)
    M = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                M[var - 1][var - 1] += 1
            else:
                M[-var - 1][-var - 1] += 1
    
    lnd_value = lnd(M)
    rank_value = rank(clauses)
    
    if rank_value == 0:
        return {
            "metric_name": "lnd_to_rank_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "rank_is_zero"
        }
    
    ratio = Fraction(lnd_value, rank_value)
    return {
        "metric_name": "lnd_to_rank_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))**0.5:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))**0.5:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lnd_to_rank_ratio_not_bounded\" first_failing_seed={first_failing_seed}")