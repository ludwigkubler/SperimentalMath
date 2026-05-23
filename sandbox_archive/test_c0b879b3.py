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
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        pivot = A[rank][j]
        for i in range(rank + 1, m):
            factor = Fraction(A[i][j], pivot)
            for j2 in range(n):
                A[i][j2] -= factor * A[rank][j2]
        rank += 1
    return rank

def matrix_rank(matrix):
    if not matrix or not matrix[0]:
        return 0
    m, n = len(matrix), len(matrix[0])
    A_copy = [row[:] for row in matrix]
    return gaussian_elimination(A_copy)

def construct_quasi_group(n):
    G = {}
    elements = list(range(1, n + 2))
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            G[(i, j)] = (i * j) % (n + 1)
    return G

def dpll_search_tree(k, clauses):
    if not clauses:
        return 0
    literals = set()
    for clause in clauses:
        literals.update(clause)
    for literal in literals:
        new_clauses = [clause for clause in clauses if literal not in clause and -literal not in clause]
        depth = dpll_search_tree(k, new_clauses) + 1
        if depth > k:
            return depth
    return k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            k = random.randint(3, 6)
            clauses = [[random.randint(1, n) for _ in range(random.randint(1, k))] for _ in range(n)]
            G = construct_quasi_group(n)
            rank = matrix_rank(G)
            depth = dpll_search_tree(k, clauses)
            results.append((rank, depth))
    
    if not results:
        return {
            "metric_name": "Rank vs DPLL Depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    ranks = [r for r, _ in results]
    depths = [d for _, d in results]
    correlation_coefficient = sum((r - mean(ranks)) * (d - mean(depths)) for r, d in results) / math.sqrt(sum((r - mean(ranks))**2 for r in ranks) * sum((d - mean(depths))**2 for d in depths))
    mean_rank = mean(ranks)
    mean_depth = mean(depths)
    max_abs_diff = max(abs(r - d) for r, d in results)
    
    return {
        "metric_name": "Rank vs DPLL Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and max_abs_diff <= 3,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = mean([r["metric_value"] for r in results])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No seeds tested")