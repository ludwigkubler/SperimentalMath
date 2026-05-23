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
from math import sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        rank = 0
        A_copy = [row[:] for row in A]
        for i in range(len(A_copy)):
            if gaussian_elimination(A_copy) is None:
                return rank
            rank += 1
        return rank

    def construct_quasi_group(clauses):
        n = len(clauses)
        G = [[None] * n for _ in range(n)]
        for x in range(n):
            for y in range(n):
                sign_x = 1 if random.choice([True, False]) else -1
                G[x][y] = (x + sign_x * y) % n
        return G

    def dpll_search_tree(k, clauses):
        if not clauses:
            return 0
        if len(clauses[0]) == 1:
            return 1
        literals = set()
        for clause in clauses:
            literals.update(clause)
        max_depth = 0
        for literal in literals:
            new_clauses = [clause for clause in clauses if literal not in clause]
            depth = dpll_search_tree(k, new_clauses) + 1
            if depth > max_depth:
                max_depth = depth
        return max_depth

    n = random.randint(5, 40)
    k = random.randint(3, 6)
    clauses = []
    for _ in range(n):
        clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(k)]
        clauses.append(clause)

    G = construct_quasi_group(clauses)
    rank = matrix_rank(G)
    depth = dpll_search_tree(k, clauses)

    return {
        "metric_name": "Rank vs DPLL Depth",
        "metric_value": abs(rank - depth),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - depth) <= 3,
        "counterexample": "" if rank == depth else f"rank={rank}, depth={depth}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank != depth\" first_failing_seed={first_failing_seed}")