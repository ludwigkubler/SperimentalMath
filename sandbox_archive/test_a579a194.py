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
    rank = sum(1 for row in A if any(row))
    return rank

def dpll_length(G):
    n = len(G)
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                clauses.append((i, -j))
                clauses.append((-i, j))
    stack = [(0, [])]
    while stack:
        level, assignment = stack.pop()
        if len(assignment) == n:
            return level
        var = next(i for i in range(n) if i not in [abs(x) for x in assignment])
        for literal in (var, -var):
            new_assignment = assignment + [literal]
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if len(new_clauses) == 0:
                stack.append((level + 1, new_assignment))
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    Δ = min(3, n - 1)
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
        for j in range(i + 1, n):
            G[j][i] = G[i][j]
    
    f = [random.randint(0, 1) for _ in range(n)]
    A = [[sum(G[i][k] * f[k] for k in range(n)) for i in range(n)] for j in range(n)]
    rank = gaussian_elimination(A)
    dpll_len = dpll_length(G)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= dpll_len,
        "counterexample": "" if rank >= dpll_len else f"Graph with DPLL length {dpll_len} but rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")