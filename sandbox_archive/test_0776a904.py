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

def rank(A):
    rref = gaussian_elimination([row[:] for row in A])
    return sum(1 for row in rref if any(row))

def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det_val = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_val += ((-1) ** j) * A[0][j] * det(submatrix)
    return det_val

def permanent(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    perm_val = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        perm_val += A[0][j] * permanent(submatrix)
    return perm_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    variables = list(range(n))
    clauses = [random.sample(variables, 3) for _ in range(10)]
    incidence_matrix = [[int(i in clause) for i in variables] for clause in clauses]
    
    det_poly = []
    perm_poly = []
    for i in range(n):
        det_poly.append(det([[incidence_matrix[j][k] if j != i else 1 for k in range(n)] for j in range(n)]))
        perm_poly.append(permanent([[incidence_matrix[j][k] if j != i else 1 for k in range(n)] for j in range(n)]))
    
    det_ideal = [det_poly]
    perm_ideal = [perm_poly]
    
    det_rank = rank(det_ideal)
    perm_rank = rank(perm_ideal)
    
    metric_value = perm_rank - det_rank
    conjecture_holds = metric_value >= 2 ** n / 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Dimension Gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")