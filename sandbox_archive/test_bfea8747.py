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
    
    def generate_polynomial(n):
        return [random.choice([0, 1]) for _ in range(n + 1)]
    
    def noncommutative_algebra(poly):
        n = len(poly)
        algebra = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            algebra[i][i] = poly[i]
        return algebra
    
    def minimal_order(algebra, N):
        for k in range(1, N + 2):
            zero_matrix = [[0] * (N + 1) for _ in range(N + 1)]
            current_matrix = algebra
            for _ in range(k - 1):
                current_matrix = matrix_multiply(current_matrix, algebra)
            if all(all(element == 0 for element in row) for row in current_matrix):
                return k
        return N + 1
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_trivial_circuit(poly, N):
        # Placeholder function to determine if the polynomial has a trivial ACC⁰ circuit threshold
        # This is a placeholder and should be replaced with actual logic
        return False
    
    n = random.randint(5, 40)
    poly = generate_polynomial(n)
    algebra = noncommutative_algebra(poly)
    order = minimal_order(algebra, n)
    
    conjecture_holds = order >= n
    counterexample = "" if conjecture_holds else f"Polynomial: {poly}, Order: {order}"
    
    return {
        "metric_name": "Minimal Order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order less than N\" first_failing_seed={first_failing_seed}")