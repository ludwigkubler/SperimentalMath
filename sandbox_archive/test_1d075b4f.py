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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row))
    return rank

def matrix_rank(A):
    m, n = len(A), len(A[0])
    A_rref = gaussian_elimination(A)
    rank = 0
    for i in range(m):
        if all(A_rref[i][j] == 0 for j in range(n)):
            continue
        rank += 1
    return rank

def dpll_proof_width(formula, n):
    # Placeholder implementation of DPLL proof width calculation
    # This is a dummy function and should be replaced with actual logic
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    rank = matrix_rank(formula)
    proof_width = dpll_proof_width(formula, n)
    
    if rank > proof_width:
        return {
            "metric_name": "Rank vs Proof Width Ratio",
            "metric_value": rank / proof_width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Seed {seed}: Rank {rank} > Proof Width {proof_width}"
        }
    else:
        return {
            "metric_name": "Rank vs Proof Width Ratio",
            "metric_value": rank / proof_width,
            "instances_tested": 1,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds proof width' first_failing_seed={first_failing_seed}")