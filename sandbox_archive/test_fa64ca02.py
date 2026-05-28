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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        for j in range(n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for k in range(n):
        max_row = max(range(k, n), key=lambda i: abs(M[i][k]))
        M[k], M[max_row] = M[max_row], M[k]
        pivot = M[k][k]
        for j in range(k, n + 1):
            M[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = M[i][k]
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]
    return [row[-1] for row in M]

def grothendieck_witt_class(poly, mod):
    n = len(poly)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            A[i][j] = (poly[i] + poly[j]) % mod
            A[j][i] = A[i][j]
    det = 1
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            return None
        det *= pivot
        for j in range(i+1, n):
            factor = A[j][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return det

def resolution_width(F):
    # Simplified DPLL solver to estimate resolution width
    def dpll(clauses, assignment):
        if not clauses:
            return 1
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            width = dpll([c for c in clauses if literal not in c], new_assignment)
            if width is None:
                return None
            new_assignment[literal] = False
            new_assignment[-literal] = True
            width = dpll([c for c in clauses if -literal not in c], new_assignment)
            if width is None:
                return None
            return max(width, 2)
        pure_literals = [l for l in range(1, len(clauses)+1) if all(l not in c or -l not in c for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            width = dpll([c for c in clauses if literal not in c], new_assignment)
            if width is None:
                return None
            new_assignment[literal] = False
            new_assignment[-literal] = True
            width = dpll([c for c in clauses if -literal not in c], new_assignment)
            if width is None:
                return None
            return max(width, 2)
        literal = random.choice([l for l in range(1, len(clauses)+1) if l not in assignment and -l not in assignment])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        width = dpll([c for c in clauses if literal not in c], new_assignment)
        if width is None:
            return None
        new_assignment[literal] = False
        new_assignment[-literal] = True
        width = dpll([c for c in clauses if -literal not in c], new_assignment)
        if width is None:
            return None
        return max(width, 2)
    assignment = [False]*(len(F)+1)
    return dpll(F, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n*3)
    k = 2
    F = []
    for _ in range(m):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = -clause[0], -clause[1]
        F.append(clause)
    
    tropical_curve_rank = grothendieck_witt_class(F, 2)
    if tropical_curve_rank is None:
        return {
            "metric_name": "tropical_curve_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    resolution_width_val = resolution_width(F)
    if resolution_width_val is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "tropical_curve_rank",
        "metric_value": tropical_curve_rank,
        "instances_tested": 1,
        "conjecture_holds": resolution_width_val <= 1.2 * tropical_curve_rank,
        "counterexample": "" if resolution_width_val <= 1.2 * tropical_curve_rank else f"resolution_width={resolution_width_val} > 1.2 * tropical_curve_rank={1.2 * tropical_curve_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    avg_metric_value = total_metric_value / len(results) if any(r["metric_value"] is not None for r in results) else 0
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results) if any(r["metric_value"] is not None for r in results) else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")