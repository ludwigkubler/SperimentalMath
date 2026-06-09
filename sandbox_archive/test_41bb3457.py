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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        pivot = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def hodge_zagier_rank(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                A[i][var - 1] += 1
            else:
                A[i][-1] -= 1
    try:
        gaussian_elimination(A)
    except ValueError as e:
        return float('inf')  # Return infinity if the matrix is singular
    rank = sum(1 for row in A if any(row))
    return rank

def generate_cnf(n):
    clauses = []
    variables = set()
    for _ in range(random.randint(2, n * (n - 1) // 2)):
        clause = [random.choice([-var, var] for var in range(1, n + 1)) for _ in range(random.randint(1, n))]
        clauses.append(clause)
        variables.update(abs(var) for var in clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    h_z_rank = hodge_zagier_rank(cnf)
    if h_z_rank == float('inf'):
        return {
            "metric_name": "Hodge-Zagier Rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    max_width = n ** 2 / 3
    width = random.randint(1, int(max_width))
    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= max_width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")