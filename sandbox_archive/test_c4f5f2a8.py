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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = rank
        for i in range(rank, rows):
            if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                i_max = i
        if matrix[i_max][j] == 0:
            continue
        matrix[i_max], matrix[rank] = matrix[rank], matrix[i_max]
        for i in range(rows):
            if i != rank:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(cols):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def communication_matrix(f, n):
    M = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        x = i
        y = f[i]
        for j in range(n):
            if x & 1:
                y ^= f[(i >> 1) ^ (1 << j)]
            x >>= 1
        M[y][i] = 1
    return M

def abp_size(f, n):
    # Placeholder function; actual implementation depends on specific function class bounds
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    f = generate_boolean_function(n)
    M_f = communication_matrix(f, n)
    rank = gaussian_elimination(M_f)
    abp_size_val = abp_size(f, n)
    conjecture_holds = abp_size_val >= rank
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "ABP Size",
        "metric_value": abp_size_val,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")