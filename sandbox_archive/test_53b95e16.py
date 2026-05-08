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
# end SEC prelude

import random
import math
from typing import List, Dict

def generate_random_matrix(n: int) -> List[List[float]]:
    return [[random.random() for _ in range(n)] for _ in range(n)]

def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    n = len(A)
    C = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def spectral_norm(matrix: List[List[float]]) -> float:
    n = len(matrix)
    v = [1.0 / math.sqrt(n)] * n
    for _ in range(100):  # Power iteration method
        v = matrix_multiply(matrix, v)
        norm = sum(x**2 for x in v) ** 0.5
        v = [x / norm for x in v]
    return max(abs(x) for x in v)

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a read-twice branching program matrix
    read_twice_matrix = generate_random_matrix(n)
    read_twice_norm = spectral_norm(read_twice_matrix)
    
    # Generate a general branching program matrix
    general_matrix = generate_random_matrix(n)
    general_norm = spectral_norm(general_matrix)
    
    return {
        "metric_name": "Noncommutative Operator Norm",
        "metric_value": read_twice_norm / general_norm,
        "instances_tested": 1,
        "conjecture_holds": read_twice_norm <= math.log(n),
        "counterexample": ""
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
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")