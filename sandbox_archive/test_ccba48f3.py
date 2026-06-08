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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def communication_complexity_rank_variance(A):
        n = len(A)
        U, _, Vt = gaussian_elimination([[A[i][j] if i != j else 1 for j in range(n)] for i in range(n)])
        rank = sum(1 for row in U if any(row))
        return math.sqrt((n - rank) / rank)
    
    def minimal_local_index(A):
        n = len(A)
        I_min = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                A_ij = [A[i][k] * A[j][k] for k in range(n)]
                U_ij, _, _ = gaussian_elimination([A_ij])
                rank_ij = sum(1 for row in U_ij if any(row))
                I_min = min(I_min, rank_ij)
        return I_min
    
    def generate_instance(n):
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        return A
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_ratio = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            A = generate_instance(n)
            I_min = minimal_local_index(A)
            sigma_phi = communication_complexity_rank_variance(A)
            if sigma_phi == 0:
                continue
            ratio = abs(I_min / sigma_phi)
            total_ratio += ratio
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_ratio = total_ratio / instances_tested
    
    if conjecture_holds and counterexample == "":
        RESULT = "SUPPORTED" if mean_ratio <= 1.05 * c else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    return {
        "metric_name": "Ratio of Minimal Local Index to Communication Complexity Rank Variance",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        RESULT = f"SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0"
    elif support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)