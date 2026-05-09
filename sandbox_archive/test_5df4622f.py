# auto-injected by SEC sandbox
import itertools
import collections
import json
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
from sys import argv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        instance = [random.choice([0, 1]) for _ in range(n * (n - 1) // 2)]
        return instance
    
    def adjacency_matrix(instance, n):
        A = [[0] * n for _ in range(n)]
        idx = 0
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = instance[idx]
                A[j][i] = instance[idx]
                idx += 1
        return A
    
    def power_method(A, max_iter=1000, tol=1e-6):
        n = len(A)
        x = [random.random() for _ in range(n)]
        x /= math.sqrt(sum(x[i]**2 for i in range(n)))
        
        for _ in range(max_iter):
            y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
            y_norm = math.sqrt(sum(y[i]**2 for i in range(n)))
            if abs(y_norm - 1) < tol:
                return y
            x = y
        return y
    
    def eigenvalues(A):
        n = len(A)
        eigvals = []
        for _ in range(30):  # Power method to approximate eigenvalues
            eigval = power_method(A)
            eigvals.append(eigval)
        return eigvals
    
    def sos_degree(n, eigvals):
        lambda_val = 1 / math.sqrt(n)
        count_outside_interval = sum(abs(eigval) > lambda_val for eigval in eigvals)
        return count_outside_interval
    
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    A = adjacency_matrix(instance, n)
    eigvals = eigenvalues(A)
    sos_deg = sos_degree(n, eigvals)
    
    lambda_val = 1 / math.sqrt(n)
    count_in_interval = sum(abs(eigval) <= lambda_val for eigval in eigvals)
    
    return {
        "metric_name": "eigenvalue_count",
        "metric_value": count_in_interval,
        "instances_tested": 1,
        "conjecture_holds": sos_deg >= count_outside_interval,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in argv[1:]] if argv[1:] else [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")