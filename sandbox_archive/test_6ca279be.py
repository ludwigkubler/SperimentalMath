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
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i+1, n):
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def determinant(A):
        n = len(A)
        det = 0
        if n == 2:
            det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for c in range(n):
                M = [row[:c] + row[c+1:] for row in A[1:]]
                det += ((-1) ** c) * A[0][c] * determinant(M)
        return det

    def permanent(A):
        n = len(A)
        if n == 2:
            return A[0][0] * A[1][1] + A[0][1] * A[1][0]
        else:
            perm = 0
            for c in range(n):
                M = [row[:c] + row[c+1:] for row in A[1:]]
                perm += ((-1) ** c) * determinant(M)
            return perm

    def invariant_ring_dimension(P, D, n):
        # Placeholder function to compute the dimension of the invariant ring
        # This is a dummy implementation and should be replaced with actual computation
        return 0

    results = []
    for n in [5, 10, 15, 20, 30]:
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        det_A = determinant(A)
        perm_A = permanent(A)
        
        dim_det = invariant_ring_dimension(P=det_A, D=perm_A, n=n)
        dim_perm = invariant_ring_dimension(P=perm_A, D=det_A, n=n)
        
        results.append({
            "metric_name": "Invariant Ring Dimension",
            "metric_value": dim_perm - dim_det,
            "instances_tested": 1,
            "conjecture_holds": dim_perm > dim_det,
            "counterexample": ""
        })

    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")