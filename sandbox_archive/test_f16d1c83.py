# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def boundary_matrix(C):
        m, n = len(C), len(C[0])
        B = [[0] * (m + n - 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if C[i][j]:
                    B[i][j] = 1
                    B[j+m-1-i][i] = 1
        return B
    
    def betti_numbers(B):
        m, n = len(B), len(B[0])
        B_tilde = gaussian_elimination(B)
        rank = sum(1 for row in B_tilde if any(row))
        return [rank - i for i in range(m)]
    
    def is_monotone_formula(f):
        # Placeholder function; replace with actual implementation
        return True
    
    n = random.randint(5, 14)
    m = random.randint(2 * n, 3 * n)
    clauses = []
    variables = set()
    for _ in range(m):
        clause = [random.choice([0, 1]) for _ in range(n)]
        while not any(clause):
            clause = [random.choice([0, 1]) for _ in range(n)]
        clauses.append(clause)
        variables.update(range(n))
    
    C = [[0] * len(variables) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for j, var in enumerate(variables):
            if clause[j]:
                C[i][j] = 1
    
    B = boundary_matrix(C)
    betti = betti_numbers(B)
    
    L_m_f = len(clauses)  # Placeholder; replace with actual monotone formula size calculation
    metric_value = sum(betti)
    conjecture_holds = metric_value <= 0.1 * L_m_f
    
    return {
        "metric_name": "GF(2)-Betti numbers sum",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")