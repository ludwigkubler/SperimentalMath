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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
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

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * A[0][c] * sub_det
        return det

    def log_base(x, base):
        if x <= 0 or base <= 1:
            return float('inf')
        return math.log(x) / math.log(base)

    n = random.randint(5, 40)
    variables = list(range(n))
    clauses = [random.sample(variables, random.randint(1, n)) for _ in range(n)]
    
    incidence_complex = [[i in clause for i in variables] for clause in clauses]
    
    def min_distortion_to_hyperbolic_space(complex):
        m, n = len(complex), len(complex[0])
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if complex[i][j]:
                    A[i][j] = 1
            A[i][-1] = -1
        
        A = gaussian_elimination(A)
        
        det = determinant([row[:-1] for row in A])
        return log_base(abs(det), 2)

    def dpll_search_tree_height(complex):
        m, n = len(complex), len(complex[0])
        stack = [(complex, 0)]
        max_height = 0
        
        while stack:
            current_complex, height = stack.pop()
            if all(all(row[i] for row in current_complex) for i in range(n)):
                max_height = max(max_height, height)
                continue
            var = next(i for i in range(n) if any(not row[i] for row in current_complex))
            new_complexes = [current_complex[:], current_complex[:]]
            new_complexes[0][var][random.choice([i for i, x in enumerate(current_complex[var]) if not x])] = 1
            new_complexes[1][var][random.choice([i for i, x in enumerate(current_complex[var]) if x])] = 1
            stack.extend([(new_complex, height + 1) for new_complex in new_complexes])
        
        return max_height

    distortion = min_distortion_to_hyperbolic_space(incidence_complex)
    dpll_height = dpll_search_tree_height(incidence_complex)
    
    if distortion == float('inf') or dpll_height == float('inf'):
        return {
            "metric_name": "min_distortion",
            "metric_value": distortion,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_n = math.log(n, 2)
    return {
        "metric_name": "min_distortion",
        "metric_value": distortion,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(distortion - log_n) <= log_n / 2 and 0.5 * log_n <= dpll_height <= 1.5 * log_n,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")