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
from itertools import product

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def protocol_pullback(G, protocol):
    k = len(G)
    m = len(protocol)
    pullback = [[0 for _ in range(k)] for _ in range(k)]
    for i in range(k):
        for j in range(k):
            pullback[i][j] = protocol[(i // (k-1)) % m][(j // (k-1)) % m]
    return pullback

def compute_cover_multiplicity(pullback, R):
    k = len(pullback)
    multiplicity = 0
    for i in range(k):
        for j in range(k):
            if pullback[i][j] > 0:
                multiplicity += pullback[i][j]
    return multiplicity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters
    n = 3
    k_values = [2, 3, 4, 5]
    Q_f_values = list(range(1, n+1))
    
    metric_values = []
    instances_tested = 0
    
    for k in k_values:
        G = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
        for Q_f in Q_f_values:
            f = [random.randint(0, 1) for _ in range(Q_f)]
            protocol = [[[random.randint(0, 1) for _ in range(k)] for _ in range(k)] for _ in range(len(f))]
            
            pullback = protocol_pullback(G, protocol)
            R = sum(sum(row) for row in G)
            multiplicity = compute_cover_multiplicity(pullback, R)
            
            metric_values.append(multiplicity)
            instances_tested += 1
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(x >= 2**(Q_f * n) for Q_f, x in zip(Q_f_values, metric_values[:len(Q_f_values)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Cover Multiplicity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")