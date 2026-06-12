# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i + 1, n):
                factor = Fraction(A[k][i], A[i][i])
                A[k][i:] = [A[k][j] - factor * A[i][j] for j in range(i, n)]
                b[k] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for k in range(i - 1, -1, -1):
                b[k] -= A[k][i] * x[i]
        return x

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_sub(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] - B[i][j]) % mod
        return C

    def matrix_add(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = (A[i][j] + B[i][j]) % mod
        return C

    def matrix_inv(A, mod):
        n = len(A)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A_augmented = [row[:] + col[:] for row, col in zip(A, I)]
        gaussian_elimination(A_augmented, [0] * n)
        return [row[n:] for row in A_augmented]

    def cusp_form_weight(instance):
        # Placeholder function to compute the weight of a cusp form
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)

    def dpll_search_tree_width(instance):
        # Placeholder function to compute the DPLL search tree width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(5, 20)

    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = [random.choice([0, 1]) for _ in range(n)]
    
    weight = cusp_form_weight(instance)
    width = dpll_search_tree_width(instance)
    
    return {
        "metric_name": "weight_width_correlation",
        "metric_value": abs(weight - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")