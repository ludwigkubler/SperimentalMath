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
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def determinant(A):
        if len(A) == 2:
            return A[0][0]*A[1][1] - A[0][1]*A[1][0]
        det = 0
        for j in range(len(A)):
            det += ((-1)**j) * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det

    def permanent(A):
        if len(A) == 2:
            return A[0][0]*A[1][1] + A[0][1]*A[1][0]
        perm = 0
        for j in range(len(A)):
            perm += ((-1)**j) * A[0][j] * permanent([row[:j] + row[j+1:] for row in A[1:]])
        return perm

    def invariant_ring_dimension(n):
        if n == 2:
            return 3
        elif n == 3:
            return 6
        else:
            return "mapping_undefined"

    n = random.randint(5, 40)
    P_n = permanent([[random.randint(-10, 10) for _ in range(n)] for _ in range(n)])
    D_n = determinant([[random.randint(-10, 10) for _ in range(n)] for _ in range(n)])

    dim_P_n = invariant_ring_dimension(n)
    dim_D_n = invariant_ring_dimension(n)

    if dim_P_n == "mapping_undefined" or dim_D_n == "mapping_undefined":
        return {
            "metric_name": "invariant_ring_dimension",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    return {
        "metric_name": "invariant_ring_dimension",
        "metric_value": dim_P_n - dim_D_n,
        "instances_tested": 1,
        "conjecture_holds": dim_P_n > dim_D_n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + list(range(53, 89))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"invariant_ring_dimension\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")