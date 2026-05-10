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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = M[j][i] = 1
    return M

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            M[j][i:] = [M[j][k] - factor * M[i][k] for k in range(i, n + 1)]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][-1] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for c in range(n):
        det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
    return det

def genus_of_hyperelliptic_curve(A):
    n = len(A)
    if n % 2 != 1:
        return None
    d = n // 2
    B = [[A[i][j] for j in range(d + 1)] for i in range(d + 1)]
    det_B = determinant(B)
    genus = (d - 1) * (d - 2) // 2 - det_B / 2
    return genus

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    f_coeffs = [sum(M[i][j] for i in range(n)) for j in range(n)]
    
    # Compute the genus using an explicit formula for hyperelliptic curves
    genus = genus_of_hyperelliptic_curve(M)
    if genus is None:
        return {
            "metric_name": "genus",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lower_bound = math.log2(1 + 2**(n/2)) - 2
    conjecture_holds = genus >= lower_bound
    
    return {
        "metric_name": "genus",
        "metric_value": genus,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Genus {genus} < {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_genus = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_genus)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_genus} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")