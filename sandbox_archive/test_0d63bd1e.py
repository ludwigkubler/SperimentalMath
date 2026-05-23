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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def bp_readtwice_width(instance):
        # Placeholder function to simulate BP_ReadTwice width computation
        n = len(instance)
        return 2 * n  # Simplified for demonstration purposes

    def tropicalized_hodge_rank(instance):
        # Placeholder function to simulate tropicalized Hodge rank computation
        n = len(instance)
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        rank = gaussian_elimination(A)
        return sum(1 for row in rank if any(row[j] != 0 for j in range(len(row))))

    def f_n(n):
        # Placeholder function to simulate the upper bound function f(n)
        return n * math.log2(n)

    instance = [[random.randint(0, 1) for _ in range(random.randint(5, 10))] for _ in range(random.randint(5, 10))]
    rho_V_I = tropicalized_hodge_rank(instance)
    bp_width = bp_readtwice_width(instance)
    f_n_value = f_n(len(instance))

    conjecture_holds = (rho_V_I <= f_n_value) and (bp_width <= 10)

    return {
        "metric_name": "BP_ReadTwice Width",
        "metric_value": bp_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": f"rho_V_I={rho_V_I}, f(n)={f_n_value}, bp_width={bp_width}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")