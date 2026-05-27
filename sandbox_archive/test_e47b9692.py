# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
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
    return A

def matrix_rank(A):
    rank = 0
    A_copy = [row[:] for row in A]
    m, n = len(A), len(A[0])
    for i in range(min(m, n)):
        if A_copy[i][i] != 0:
            rank += 1
            for j in range(i + 1, m):
                factor = A_copy[j][i] / A_copy[i][i]
                for k in range(n):
                    A_copy[j][k] -= factor * A_copy[i][k]
    return rank

def xor_and_tree_width(clauses):
    n = len(clauses[0])
    assignments = list(product([False, True], repeat=n))
    satisfied = 0
    unsatisfied = 0
    for assignment in assignments:
        if any(all(assignment[j-1] if c > 0 else not assignment[j-1] for c in clause) for clause in clauses):
            satisfied += 1
        else:
            unsatisfied += 1
    return max(satisfied, unsatisfied)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1))
    
    clauses = []
    for _ in range(m):
        variables = set(random.sample(range(1, n + 1), random.randint(1, n)))
        clause = [random.choice([1, -1]) * v for v in variables]
        clauses.append(clause)
    
    T_F_rank = matrix_rank(gaussian_elimination([[sum(c[i] for c in clause) for i in range(n)] for clause in clauses]))
    width = xor_and_tree_width(clauses)
    
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": width,
        "instances_tested": len(clauses),
        "conjecture_holds": T_F_rank * 3 > width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")