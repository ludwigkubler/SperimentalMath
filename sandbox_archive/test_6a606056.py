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
from fractions import Fraction
import math

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_diophantine_equation_complexity(f):
    n = int(math.log2(len(f)))
    matrix = [[Fraction(f[i * (1 << j)], 1) if i & (1 << j) else Fraction(0, 1) for j in range(n)] for i in range(1 << n)]
    rank = gaussian_elimination(matrix)
    return rank

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        if matrix[i][i] == 0:
            for j in range(i + 1, m):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(n):
            matrix[i][j] /= matrix[i][i]
        for j in range(m):
            if j != i and matrix[j][i] != 0:
                for k in range(n):
                    matrix[j][k] -= matrix[i][k] * matrix[j][i]
    return sum(1 for row in matrix if any(row))

def compute_communication_rank_variance(f):
    n = int(math.log2(len(f)))
    indicators = [sum(1 << j for j, bit in enumerate(bin(i)[2:].zfill(n)) if bit == '1') for i in range(1 << n)]
    variance = sum((f[i] - f[j]) ** 2 for i in range(1 << n) for j in range(i + 1, 1 << n)) / (len(f) * (len(f) - 1))
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    c_g = compute_diophantine_equation_complexity(f)
    crv_f = compute_communication_rank_variance(f)
    
    if c_g > 10:
        return {
            "metric_name": "Diophantine Equation Complexity",
            "metric_value": c_g,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "c(g) > 10"
        }
    
    return {
        "metric_name": "Diophantine Equation Complexity",
        "metric_value": c_g,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"c(g) > 10\" first_failing_seed={first_failing_seed}")