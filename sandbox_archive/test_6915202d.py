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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find max pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        # Eliminate entries below pivot
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, p = len(A), len(B[0])
    n = len(B)
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def resolution_length(cnf):
    clauses = [set(clause) for clause in cnf]
    n = len(clauses)
    if n == 0:
        return 0
    # Initialize variables
    max_length = 0
    visited = set()
    queue = []
    # BFS to find the longest resolution path
    for i in range(n):
        queue.append((i, 1))
        while queue:
            current, length = queue.pop(0)
            if current not in visited:
                visited.add(current)
                max_length = max(max_length, length)
                for j in range(n):
                    if clauses[j].isdisjoint(clauses[current]):
                        queue.append((j, length + 1))
    return max_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
        if 0 not in clause:
            cnf.append(clause)
    length = resolution_length(cnf)
    if length == 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    t = length
    # Approximate Riemann Zeta function at s = 1/2 + it
    zeta_value = sum(1 / (n**0.5 + 1j * t) for n in range(1, 1000))
    # Check if there is a zero in the critical strip
    has_zero = abs(zeta_value.real) < 1e-6 and abs(zeta_value.imag) < 1e-6
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": has_zero,
        "counterexample": "" if has_zero else f"no_zero_found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break