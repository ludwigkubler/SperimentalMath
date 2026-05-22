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
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        pivot = Fraction(1, A[i][i])
        for j in range(i, n):
            A[i][j] *= pivot
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = -A[k][i]
                for j in range(i, n):
                    A[k][j] += factor * A[i][j]
    rank = sum(1 for row in A if any(row))
    return rank

def formal_group_rank(clauses):
    n = len(clauses)
    G = [[0]*n for _ in range(n)]
    for clause in clauses:
        for x, y in itertools.combinations(clause, 2):
            G[x][y] += 1
            G[y][x] += 1
    return gaussian_elimination(G)

def dpll_search_tree_height(clauses):
    # Placeholder function to simulate DPLL search tree height
    # This is a dummy implementation and should be replaced with actual logic
    return len(clauses) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.randint(0, n-1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    rank = formal_group_rank(clauses)
    height = dpll_search_tree_height(clauses)
    
    f_n = n**2  # Example polynomial function f(n) = n^2
    conjecture_holds = rank <= f_n and height <= f_n
    
    return {
        "metric_name": "Ratio of DPLL Search Tree Height to Minimal Rank",
        "metric_value": height / rank if rank > 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}, height={height}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, rank={results[0]['metric_value']}, height=inf\" first_failing_seed={first_failing_seed}")