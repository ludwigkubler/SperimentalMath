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
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i ^ (1 << j) < n:
                    A[i][j] = f[(i ^ (1 << j))]
                else:
                    A[i][j] = 0
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_power(A, k):
        n = len(A)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        while k > 0:
            if k % 2 == 1:
                result = matrix_multiplication(result, A)
            A = matrix_multiplication(A, A)
            k //= 2
        return result
    
    def minimal_order_of_local_units(A):
        n = len(A)
        identity = [[0] * n for _ in range(n)]
        for i in range(n):
            identity[i][i] = 1
        
        order = 1
        current_matrix = A
        while True:
            if matrix_power(current_matrix, order) == identity:
                return order
            order += 1
    
    def circuit_entanglement_complexity(f):
        n = len(f)
        # Simplified heuristic for demonstration purposes
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(1 << n)]
    
    A = characteristic_polynomial(f)
    try:
        order = minimal_order_of_local_units(A)
    except Exception as e:
        return {
            "metric_name": "minimal_order_of_local_units",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    e = circuit_entanglement_complexity(f)
    
    return {
        "metric_name": "minimal_order_of_local_units",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next((result["seed"] for result in results if result["metric_value"] is None), None)
        RESULT = f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)