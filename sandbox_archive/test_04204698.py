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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def euclidean_distance(x, y):
        return sum((a - b)**2 for a, b in zip(x, y)) ** 0.5
    
    def calculate_curvature_tensor(X):
        n = len(X)
        if n < 3:
            return None
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d_ij = euclidean_distance(X[i], X[j])
                if d_ij == 0:
                    continue
                for k in range(j + 1, n):
                    d_ik = euclidean_distance(X[i], X[k])
                    d_jk = euclidean_distance(X[j], X[k])
                    if d_ik == 0 or d_jk == 0:
                        continue
                    H[i][j] += (d_ij * d_jk - d_ik**2) / (d_ij * d_ik * d_jk)
        return H
    
    def is_positive_semi_definite(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] < 0:
                return False
            for j in range(i + 1, n):
                sum_k = sum(matrix[k][i] * matrix[k][j] for k in range(n))
                if not (matrix[i][j] - sum_k) >= 0:
                    return False
        return True
    
    def lower_bound_curvature(n):
        return math.sqrt(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_xor_function(n)
        X = [[f[i] ^ f[j] for j in range(2**n)] for i in range(2**n)]
        curvature_tensor = calculate_curvature_tensor(X)
        if curvature_tensor is None or not is_positive_semi_definite(curvature_tensor):
            results.append({"metric_value": 0, "instances_tested": 1, "conjecture_holds": False, "counterexample": "mapping_undefined"})
            continue
        lower_bound = lower_bound_curvature(n)
        if any(curvature_tensor[i][j] < lower_bound for i in range(n) for j in range(i + 1, n)):
            results.append({"metric_value": 0, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"Lower bound violated at n={n}"})
        else:
            results.append({"metric_value": lower_bound, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""})
    
    metric_values = [result["metric_value"] for result in results]
    instances_tested = sum(result["instances_tested"] for result in results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    
    return {
        "metric_name": "Riemannian Curvature Tensor Lower Bound",
        "metric_value": sum(metric_values) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Lower bound violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")