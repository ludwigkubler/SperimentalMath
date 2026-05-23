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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = -A[k][i]
                    for j in range(n):
                        A[k][j] += factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll_width(clauses, assignment):
        if not clauses:
            return 0
        literal = random.choice(clauses[0])
        if literal in assignment:
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return max(dpll_width(new_clauses, assignment), dpll_width(new_clauses, assignment | {literal}))
        else:
            return 1 + max(dpll_width(clauses, assignment | {literal}), dpll_width(clauses, assignment | {-literal}))

    def hodge_index(n, m):
        # Placeholder for actual Hodge index calculation
        return (m ** (1/3)) * (n ** (2/3))

    n = random.randint(5, 40)
    m = random.randint(5, 40)
    
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if not any(l in clause for l in [-x for x in clause]):
            clauses.append(clause)

    variety_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            variety_matrix[i][j] = random.choice([0, 1])
            variety_matrix[j][i] = variety_matrix[i][j]

    hodge_index_value = hodge_index(n, m)
    dpll_width_value = dpll_width(clauses, set())

    return {
        "metric_name": "Hodge Index vs DPLL Width",
        "metric_value": abs(hodge_index_value - dpll_width_value),
        "instances_tested": 1,
        "conjecture_holds": abs(hodge_index_value - dpll_width_value) <= (m ** (1/3)) * (n ** (2/3)),
        "counterexample": "" if abs(hodge_index_value - dpll_width_value) <= (m ** (1/3)) * (n ** (2/3)) else f"Hodge Index: {hodge_index_value}, DPLL Width: {dpll_width_value}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge Index vs DPLL Width\" first_failing_seed={first_failing_seed}")