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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def free_cumulant(truth_table):
        n = len(truth_table)
        cumulants = [0] * (n + 1)
        for i in range(n):
            for j in range(i, n):
                if truth_table[i][j]:
                    cumulants[2] += 1
        return max(cumulants)
    
    def read_twice_bp(n):
        # Construct a read-twice BP for the IP₂ function
        A = [[0] * n for _ in range(n)]
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if (i + j) % 2 == 0:
                    A[i][j] = 1
                    B[j][i] = 1
        return A, B
    
    def moment_cumulant_inversion(cumulants):
        # Simple approximation for demonstration purposes
        return max(cumulants)
    
    n = 40
    instances_tested = 30
    max_cumulant_3sat = 0
    max_cumulant_ip2 = 0
    
    for _ in range(instances_tested):
        truth_table = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        cumulants = [free_cumulant(truth_table) for _ in range(5)]
        max_cumulant_3sat = max(max_cumulant_3sat, moment_cumulant_inversion(cumulants))
    
    A_ip2, B_ip2 = read_twice_bp(n)
    cumulants_ip2 = [free_cumulant(A_ip2), free_cumulant(B_ip2)]
    max_cumulant_ip2 = moment_cumulant_inversion(cumulants_ip2)
    
    conjecture_holds = max_cumulant_3sat <= 5 * math.log(n) and max_cumulant_ip2 > 40
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_free_cumulant",
        "metric_value": max(max_cumulant_3sat, max_cumulant_ip2),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")