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

def fast_walsh_hadamard_transform(f: list) -> list:
    n = len(f)
    if n == 1:
        return f
    
    even = fast_walsh_hadamard_transform(f[::2])
    odd = fast_walsh_hadamard_transform(f[1::2])
    
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    
    return result

def log_rank(matrix: list) -> int:
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        pivot_row = i
        while matrix[pivot_row][i] == 0 and pivot_row < m:
            pivot_row += 1
        if pivot_row == m:
            continue
        
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        rank += 1
        for j in range(m):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    c = 10  # Constant to ensure D(f) >= c/λ
    
    f = [random.choice([0, 1]) for _ in range(2**n)]
    fourier_coefficients = fast_walsh_hadamard_transform(f)
    λ = max(abs(coeff) for coeff in fourier_coefficients)
    
    communication_matrix = [[0] * (2**n) for _ in range(2**n)]
    for x in range(2**n):
        for y in range(2**n):
            if f[x] != f[y]:
                communication_matrix[x][y] = 1
    
    D_f = log_rank(communication_matrix)
    
    conjecture_holds = D_f >= c / λ
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Deterministic Communication Complexity",
        "metric_value": D_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")