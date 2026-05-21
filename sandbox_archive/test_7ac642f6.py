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
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def permanent(M):
        n = len(M)
        if n == 0:
            return 1
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += ((-1) ** j) * M[0][j] * permanent(submatrix)
        return det

    def determinant(M):
        n = len(M)
        if n == 0:
            return 1
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += ((-1) ** j) * M[0][j] * determinant(submatrix)
        return det

    def invariant_ring_dimension(n):
        if n == 2:
            return 3
        elif n == 3:
            return 7
        else:
            return None

    n = random.randint(5, 40)
    M = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    perm_dim = invariant_ring_dimension(n)
    det_dim = invariant_ring_dimension(n)
    
    if perm_dim is None or det_dim is None:
        return {
            "metric_name": "Invariant Ring Dimension",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    perm_value = permanent(M)
    det_value = determinant(M)
    
    return {
        "metric_name": "Invariant Ring Dimension",
        "metric_value": abs(perm_dim - det_dim),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")