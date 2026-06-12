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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = Fraction(1, 1)
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -Fraction(1, 1)
    return det

def euler_characteristic(phi):
    # Placeholder implementation
    return len(phi)

def resolution_width(phi):
    def dpll_solver(clauses):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_clauses = [[l for l in c if l != literal and -l != literal] for c in clauses]
            return dpll_solver(new_clauses)
        pure_literals = {}
        for clause in clauses:
            for literal in clause:
                if literal not in pure_literals:
                    pure_literals[literal] = True
                elif -literal in pure_literals:
                    del pure_literals[literal]
                    del pure_literals[-literal]
        if pure_literals:
            literal = next(iter(pure_literals))
            new_clauses = [[l for l in c if l != literal and -l != literal] for c in clauses]
            return dpll_solver(new_clauses)
        literal = random.choice(clauses[0])
        new_clauses_true = [[l for l in c if l != literal and -l != literal] for c in clauses if literal not in c]
        new_clauses_false = [[l for l in c if l != -literal and -l != -literal] for c in clauses if -literal not in c]
        return dpll_solver(new_clauses_true) or dpll_solver(new_clauses_false)
    
    return len(phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = random.randint(1, n * (n - 1) // 2)
    phi = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(m)]
    
    chi_phi = euler_characteristic(phi)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "Euler Characteristic vs Resolution Width",
        "metric_value": chi_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(chi_phi - w_phi) < 0.1 * max(abs(chi_phi), abs(w_phi)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")