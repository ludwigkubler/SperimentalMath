# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def tropical_zero():
    return float('-inf')

def tropical_add(a, b):
    if a == tropical_zero() or b == tropical_zero():
        return max(a, b)
    else:
        return max(a + b, 0)

def tropical_mul(a, b):
    if a == tropical_zero() or b == tropical_zero():
        return tropical_zero()
    else:
        return a + b

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for k in range(m):
            A[i][k] /= A[i][i]
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(m):
                    A[j][k] -= factor * A[i][k]
    return A

def tropical_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for i in range(n):
        if all(abs(A[j][i]) == tropical_zero() for j in range(n)):
            continue
        rank += 1
    return rank

def generate_tropical_circuit(n, m):
    A = [[random.choice([tropical_zero(), random.randint(-10, 10)]) for _ in range(m)] for _ in range(n)]
    B = [random.choice([tropical_zero(), random.randint(-10, 10)]) for _ in range(m)]
    return A, B

def phase_cells(A, B):
    n = len(A)
    m = len(B)
    cells = set()
    for i in range(2**n):
        x = [int(bit) for bit in f"{i:0{n}b}"]
        y = sum(x[j] * A[j][k] for j, k in enumerate(range(m))) + B
        cell = tuple(sorted(y))
        cells.add(cell)
    return len(cells)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        A, B = generate_tropical_circuit(n, n)
        tropical_rank_value = tropical_rank(A)
        phase_cell_count = phase_cells(A, B)
        results.append({
            "n": n,
            "tropical_rank_value": tropical_rank_value,
            "phase_cell_count": phase_cell_count
        })
    metric_name = "Phase Cell Count"
    metric_value = sum(result["phase_cell_count"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["phase_cell_count"] <= result["tropical_rank_value"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")