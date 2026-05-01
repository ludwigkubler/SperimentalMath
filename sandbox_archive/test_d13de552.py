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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def abp_size(f, n):
        if n == 1:
            return 1
        size = float('inf')
        for i in range(n):
            for j in range(i+1, n):
                f_i_j = [f[i] ^ f[j] for i, j in zip(range(2**n), range(2**n))]
                size = min(size, abp_size(f_i_j[:2**(i+j)], i+j) + 1)
        return size
    
    def permutation_polynomial_degree(f, n):
        x = [random.randint(0, 2**n - 1) for _ in range(n)]
        y = [f[i] for i in range(2**n)]
        A = []
        for j in range(n):
            row = []
            for i in range(2**n):
                row.append(x[j] ^ x[(i + (1 << j)) % 2**n])
            A.append(row)
        B = y[:]
        for _ in range(n):
            pivot_col = max(range(n), key=lambda col: abs(sum(A[row][col] for row in range(2**n))))
            if A[0][pivot_col] == 0:
                return float('inf')
            for i in range(1, 2**n):
                factor = A[i][pivot_col] / A[0][pivot_col]
                for j in range(n):
                    A[i][j] -= factor * A[0][j]
                B[i] -= factor * B[0]
            A.pop(0)
            B.pop(0)
        return n
    
    n = 40
    f = generate_boolean_function(n)
    abp_s = abp_size(f, n)
    poly_d = permutation_polynomial_degree(f, n)
    
    if poly_d > abp_s or poly_d < abp_s / math.log(n):
        return {
            "metric_name": "degree",
            "metric_value": poly_d,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"ABP size: {abp_s}, Poly degree: {poly_d}"
        }
    
    return {
        "metric_name": "degree",
        "metric_value": poly_d,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"degree mismatch\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")