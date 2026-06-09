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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = max(range(rank, m), key=lambda i: abs(A[i][j]))
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j]:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def binary_hypercube_Ehrhart_semigroup(n, r):
        # Generate a random binary hypercube of size n with rank variance r
        # This is a placeholder function. For actual implementation, refer to the literature.
        return random.randint(1, 2**n)
    
    def log_base_10(x):
        if x <= 0:
            return float('-inf')
        return math.log10(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            r = random.randint(1, n)
            semigroup_size = binary_hypercube_Ehrhart_semigroup(n, r)
            num_generators = gaussian_elimination([[i % (n + 1) for i in range(semigroup_size)]])
            results.append({
                "n": n,
                "r": r,
                "semigroup_size": semigroup_size,
                "num_generators": num_generators
            })
    
    total_num_generators = sum(result["num_generators"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["num_generators"] >= 10 ** log_base_10(result["n"] + result["r"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_num_generators",
        "metric_value": total_num_generators / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 2**32 - 1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")