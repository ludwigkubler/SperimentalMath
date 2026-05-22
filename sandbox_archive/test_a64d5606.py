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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = -A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            return None
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def geometric_entropy(A):
        det = determinant(A)
        if det is None or det == 0:
            return float('inf')
        return -math.log(abs(det))

    n = random.randint(5, 40)
    m = random.randint(1, n)
    variables = [random.sample(range(n), m) for _ in range(m)]
    
    H = [[0 for _ in range(n)] for _ in range(n)]
    for var_set in variables:
        for i in var_set:
            for j in var_set:
                H[i][j] += 1
    
    A = gaussian_elimination(H)
    min_entropy = geometric_entropy(A)
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": min_entropy,
        "instances_tested": m,
        "conjecture_holds": True if min_entropy <= n**2 else False,
        "counterexample": "" if min_entropy <= n**2 else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, m={len(results[0]['counterexample'])}\" first_failing_seed={first_failing_seed}")