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
    
    def generate_polynomial(n, D):
        coefficients = [random.randint(0, 100) for _ in range(D + 1)]
        return coefficients
    
    def plethysm_coefficients(poly, m):
        n = len(poly) - 1
        result = [[0] * (n + 1) for _ in range(n + 1)]
        result[0][0] = poly[0]
        for i in range(1, n + 1):
            for j in range(i + 1):
                result[i][j] = sum(result[k][j - k] * poly[k] for k in range(j))
        return result
    
    def permanent_circuit_size(poly):
        n = len(poly) - 1
        if n == 0:
            return 1
        size = 0
        for i in range(1, n + 1):
            size += permanent_circuit_size(poly[:i]) * permanent_circuit_size(poly[i:])
        return size
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[j][i] == 0 for j in range(n)):
                continue
            rank += 1
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            for k in range(m):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        return rank
    
    def is_valid_seed(seed):
        random.seed(seed)
        n = 40
        D = int(math.log2(n) ** 2)
        poly = generate_polynomial(n, D)
        plethysm_coeffs = plethysm_coefficients(poly, m=10)
        perm_circuit_size = permanent_circuit_size(poly)
        return min_rank(plethysm_coeffs) >= D and perm_circuit_size <= 10 ** D
    
    if not is_valid_seed(seed):
        return {
            "metric_name": "Rank vs Perm Circuit",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = 40
    D = int(math.log2(n) ** 2)
    poly = generate_polynomial(n, D)
    plethysm_coeffs = plethysm_coefficients(poly, m=10)
    perm_circuit_size = permanent_circuit_size(poly)
    
    return {
        "metric_name": "Rank vs Perm Circuit",
        "metric_value": min_rank(plethysm_coeffs),
        "instances_tested": 1,
        "conjecture_holds": min_rank(plethysm_coeffs) >= D and perm_circuit_size <= 10 ** D,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")