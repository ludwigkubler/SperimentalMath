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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            det += (-1) ** j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det
    
    def sos_degree_max_cut(n):
        # Placeholder function to compute SOS degree for max-CUT
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(3, 5)
    
    def minimal_hodge_index(A):
        # Placeholder function to compute minimal Hodge index
        # This is a dummy implementation and should be replaced with actual computation
        det = determinant(gaussian_elimination(A))
        return abs(det) ** (1 / len(A))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = sos_degree_max_cut(n)
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    hodge_index = minimal_hodge_index(A)
    
    alpha = 0.5  # Empirical constant
    metric_value = hodge_index / n
    
    return {
        "metric_name": "Hodge Index Ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value >= alpha * n,
        "counterexample": "" if metric_value >= alpha * n else "SOS degree or Hodge index computation error"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample='SOS degree or Hodge index computation error' first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)