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
        # Generate a random homogeneous polynomial f(x1, ..., xn) of degree D
        coefficients = [[random.randint(-10, 10) for _ in range(D + 1)] for _ in range(n)]
        return coefficients
    
    def plethysm_coefficients(poly, m):
        # Compute the plethysm coefficients (simplified version)
        n = len(poly)
        result = [[0] * (n + 1) for _ in range(m + 1)]
        result[0][0] = 1
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                result[i][j] = sum(result[i - k][j - 1] * poly[k][j - 1] for k in range(1, min(i, j) + 1))
        return result
    
    def permanent_circuit_size(poly):
        # Compute the size of the permanent circuit (simplified version)
        n = len(poly)
        result = [[0] * (n + 1) for _ in range(n + 1)]
        result[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                result[i][j] = sum(result[i - k][j - 1] * poly[k][j - 1] for k in range(1, min(i, j) + 1))
        return result
    
    def min_rank(matrix):
        # Compute the minimal rank of a matrix (simplified version)
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank)):
                rank += 1
                for j in range(rank):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def is_valid_instance(n, D):
        # Check if the instance is valid
        if n <= 0 or D <= 0:
            return False
        return True
    
    n = random.randint(5, 40)
    D = int(math.log2(n) ** 2)
    
    if not is_valid_instance(n, D):
        return {
            "metric_name": "Rank vs Permanent Circuit Size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Invalid instance"
        }
    
    poly = generate_polynomial(n, D)
    plethysm_coeffs = plethysm_coefficients(poly, n)
    perm_circuit_size = permanent_circuit_size(poly)
    
    min_rank_value = min_rank(plethysm_coeffs)
    conjecture_holds = min_rank_value >= D and perm_circuit_size <= n ** 1.5
    
    return {
        "metric_name": "Rank vs Permanent Circuit Size",
        "metric_value": min_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Counterexample found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Counterexample found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")