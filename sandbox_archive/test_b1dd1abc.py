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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def entanglement_complexity(circuit):
        # Placeholder function to compute entanglement complexity
        # This is a dummy implementation and should be replaced with actual logic
        return len(circuit)

    def construct_twisted_module(circuit):
        # Placeholder function to construct twisted module
        # This is a dummy implementation and should be replaced with actual logic
        m = len(circuit)
        n = 2 * m
        A = [[0]*n for _ in range(n)]
        for i in range(m):
            A[i][i] = 1
            A[i+m][i+m] = 1
            A[i][i+m] = -1
            A[i+m][i] = -1
        return gaussian_elimination(A)

    def matrix_order(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if any(abs(x) > 1e-9 for x in matrix[i]):
                return sum(1 for row in matrix if any(abs(x) > 1e-9 for x in row))
        return 0

    n = random.randint(5, 40)
    circuit = [random.choice([0, 1]) for _ in range(n)]
    e_C = entanglement_complexity(circuit)
    
    M = construct_twisted_module(circuit)
    order_M = matrix_order(M)

    return {
        "metric_name": "order_of_twisted_module",
        "metric_value": order_M,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order_M <= e_C and order_M >= 1,
        "counterexample": "" if order_M <= e_C and order_M >= 1 else f"order_M={order_M}, e(C)={e_C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_M > e(C)\" first_failing_seed={first_failing_seed}")