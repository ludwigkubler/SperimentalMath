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
    
    def boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matroid_from_boolean_function(f):
        n = len(f)
        M = []
        for i in range(2**n):
            subset = [j for j in range(n) if (i >> j) & 1]
            M.append(subset)
        return M
    
    def alexander_defect_invariant(M):
        n = len(M[0])
        A = 0
        for i in range(2**n):
            subset = [j for j in range(n) if (i >> j) & 1]
            if all(len(subset) <= len(m) for m in M):
                A += 1
        return A
    
    def communication_complexity_rank(f):
        n = len(f)
        max_communication = 0
        for i in range(2**n):
            subset = [j for j in range(n) if (i >> j) & 1]
            comm = sum(f[j] for j in subset)
            max_communication = max(max_communication, comm)
        return max_communication
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        f = boolean_function(n)
        M = matroid_from_boolean_function(f)
        A = alexander_defect_invariant(M)
        r = communication_complexity_rank(f)
        metrics.append((A, r))
    
    if not metrics:
        return {
            "metric_name": "alexander_defect_invariant",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    A_values = [A for A, r in metrics]
    r_values = [r for A, r in metrics]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return covariance / (std_dev_x * std_dev_y) if std_dev_x * std_dev_y != 0 else 0
    
    correlation = pearson_correlation(A_values, r_values)
    
    return {
        "metric_name": "alexander_defect_invariant",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")