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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table_to_lie_algebroid(f):
        n = int(math.log2(len(f)))
        A_f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[2**i + 2**j] != f[2**i]:
                    A_f[i][j] = 1
        return A_f
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = [0] * (n + 1)
        for i in range(2**n):
            rank[sum(f[j] for j in range(n) if i & (1 << j))] += 1
        return sum((r - len(f)/2)**2 for r in rank) / n
    
    def min_root_length(A_f):
        n = len(A_f)
        root_lengths = [0] * n
        for i in range(n):
            for j in range(i, n):
                if A_f[i][j]:
                    root_lengths[i] += 1
                    root_lengths[j] += 1
        return min(root_lengths)
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_root_lengths = []
    R_vars = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        A_f = truth_table_to_lie_algebroid(f)
        min_root_lengths.append(min_root_length(A_f))
        R_vars.append(communication_complexity_rank_variance(f))
    
    if not min_root_lengths or not R_vars:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    corr_coeff = correlation_coefficient(min_root_lengths, R_vars)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")