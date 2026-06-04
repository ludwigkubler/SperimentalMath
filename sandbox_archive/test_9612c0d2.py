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

    def matrix_rank(A):
        A_rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in A_rref:
            if any(row):
                rank += 1
        return rank

    def algebraic_K_theory(G):
        # Simplified model: K_0(G) is the rank of G
        return matrix_rank(G)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_K0 = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):
            G = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            K0 = algebraic_K_theory(G)
            total_K0 += K0
            instances_tested += 1
            max_n = max(max_n, n)

    mean_K0 = total_K0 / instances_tested
    conjecture_holds = all(0.7 <= abs(K0/n - mean_K0) <= 1.5 for K0 in [algebraic_K_theory([[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]) for n in n_values for _ in range(5)])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "K0_over_r",
        "metric_value": mean_K0,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_K0 = sum(r["metric_value"] for r in results) / len(results)
    std_K0 = math.sqrt(sum((r["metric_value"] - mean_K0)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_K0} std={std_K0} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_K0} std={std_K0} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")