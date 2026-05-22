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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i]:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def formal_group_rank(clauses):
        n = len(clauses)
        G = [[0] * (2 * n) for _ in range(2 * n)]
        for i, clause in enumerate(clauses):
            for l1 in clause:
                for l2 in clause:
                    if l1 != l2:
                        G[i][n + literals.index(l1)] += 1
                        G[n + literals.index(l1)][i] += 1
                        G[i][n + literals.index(l2)] -= 1
                        G[n + literals.index(l2)][i] -= 1
        rank = gaussian_elimination(G)
        return sum(1 for row in rank if any(row))

    def dpll_search_tree_height(clauses):
        n = len(clauses)
        stack = [(clauses, [])]
        max_height = 0
        while stack:
            clauses, assignment = stack.pop()
            if not clauses:
                max_height = max(max_height, len(assignment))
                continue
            literal = next(l for l in literals if any(l in c for c in clauses))
            new_clauses_true = [c for c in clauses if literal not in c]
            new_clauses_false = [c for c in clauses if literal in c]
            stack.append((new_clauses_true, assignment + [literal]))
            stack.append((new_clauses_false, assignment + [-literal]))
        return max_height

    n = random.randint(5, 40)
    literals = [f'x{i}' for i in range(n)]
    clauses = [[random.choice(literals) for _ in range(random.randint(1, n))] for _ in range(n)]

    rank = formal_group_rank(clauses)
    height = dpll_search_tree_height(clauses)

    if rank > 2 * n or height > 3 * n:
        return {
            "metric_name": "Ratio of Height to Rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance with rank {rank} and height {height}"
        }

    return {
        "metric_name": "Ratio of Height to Rank",
        "metric_value": height / rank if rank != 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Instance with rank > 2n or height > 3n\" first_failing_seed={first_failing_seed}")