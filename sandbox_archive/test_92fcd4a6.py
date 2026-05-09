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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
            while len(set(literals)) < 3:
                literals[random.randint(0, 2)] = random.randint(0, 1)
            clauses.append(literals)
        return clauses
    
    def polynomial_system(clauses):
        n = len(clauses[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for clause in clauses:
            x, y, z = clause
            A[x][x] += 1
            A[y][y] += 1
            A[z][z] += 1
            A[x][y] -= 1
            A[x][z] -= 1
            A[y][x] -= 1
            A[y][z] -= 1
            A[z][x] -= 1
            A[z][y] -= 1
            b[x] += 1
            b[y] += 1
            b[z] += 1
        return A, b
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        return A, b
    
    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        return det
    
    def sos_refutation_degree(clauses):
        n = len(clauses[0])
        m = len(clauses)
        M = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            x, y, z = clause
            M[i][x] += 1
            M[i][y] += 1
            M[i][z] += 1
        degree = 0
        while True:
            found = False
            for j in range(m):
                if sum(M[j]) == 2:
                    M[j] = [0] * (n + 1)
                    degree += 1
                    found = True
                    break
            if not found:
                break
        return degree
    
    n = random.randint(5, 40)
    clauses = generate_3sat_instance(n)
    A, b = polynomial_system(clauses)
    A, b = gaussian_elimination(A, b)
    disc = determinant(A)
    ref_degree = sos_refutation_degree(clauses)
    
    metric_name = "disc_sos_ref"
    metric_value = disc
    instances_tested = 1
    conjecture_holds = disc >= 2**(0.3 * n) if ref_degree >= 0.5 * math.sqrt(n) else False
    counterexample = "" if conjecture_holds else f"disc={disc}, ref_degree={ref_degree}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")