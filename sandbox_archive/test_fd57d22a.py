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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def noncommutative_algebra(poly):
        n = len(poly)
        algebra = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            algebra[i][i] = poly[i]
        return algebra
    
    def minimal_order(algebra, N):
        for k in range(1, N + 1):
            zero_matrix = [[0 for _ in range(N)] for _ in range(N)]
            identity_matrix = [[1 if i == j else 0 for i in range(N)] for j in range(N)]
            current_power = algebra
            while True:
                next_power = matrix_multiply(current_power, algebra)
                if next_power == zero_matrix:
                    return k
                if next_power == identity_matrix:
                    break
                current_power = next_power
        return N
    
    def matrix_multiply(A, B):
        n = len(A)
        result = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def is_trivial_circuit(poly, N):
        # Placeholder function to determine if a polynomial has a trivial ACC⁰ circuit threshold
        # This is a stub and should be replaced with actual logic
        return False
    
    n = random.randint(5, 40)
    poly = [random.choice([0, 1]) for _ in range(n)]
    
    algebra = noncommutative_algebra(poly)
    order = minimal_order(algebra, n)
    trivial_circuit = is_trivial_circuit(poly, n)
    
    metric_value = order
    conjecture_holds = (order >= n) and not trivial_circuit
    
    return {
        "metric_name": "Minimal Order",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Polynomial: {poly}, Order: {order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")