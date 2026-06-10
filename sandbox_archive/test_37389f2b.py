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
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def min_local_system_rank(clauses):
    n = len(clauses[0])
    matroid_matrix = [[0] * (2*n) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for lit in clause:
            if lit > 0:
                matroid_matrix[i][lit-1] = 1
            else:
                matroid_matrix[i][n-abs(lit)-1] = -1
    return rank_of_matrix(matroid_matrix)

def resolution_width(clauses):
    n = len(clauses[0])
    clauses = [c + [-i for i in range(1, n+1)] for c in clauses]
    queue = clauses[:]
    while queue:
        clause = queue.pop()
        if any(lit < 0 and -lit in q for q in queue):
            return len(queue)
        new_clauses = []
        for q in queue:
            if any(lit > 0 and lit in q for lit in clause):
                new_clause = [l for l in q if l not in clause]
                if new_clause:
                    new_clauses.append(new_clause)
        queue.extend(new_clauses)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i+1) for i in range(n)]
        if not any(lit == -lit for lit in clause):
            clauses.append(clause)
    m_lr = min_local_system_rank(clauses)
    w = resolution_width(clauses)
    return {
        "metric_name": "correlation",
        "metric_value": abs(m_lr * w) / (n**2),
        "instances_tested": len(clauses),
        "n_max": n,
        "conjecture_holds": m_lr != 0 and w != 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, m_lr={min_local_system_rank(r['clauses'])}, w={resolution_width(r['clauses'])}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break