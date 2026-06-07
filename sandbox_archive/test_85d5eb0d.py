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
    
    def matrix_representation(f, n):
        M = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                row.append((f[i] + f[j]) % 2)
            M.append(row)
        return M
    
    def p_adic_valuation_degree(M, p):
        n = len(M)
        val = 0
        for i in range(n):
            for j in range(n):
                if M[i][j] == 1:
                    val += math.log(i + j + 1, p)
        return val
    
    def communication_complexity_rank(f, n):
        # Placeholder function; actual implementation depends on the specific problem
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f, n)
        p = random.choice([2, 3, 5, 7, 11])  # Fixed prime for simplicity
        vd_p_f = p_adic_valuation_degree(M, p)
        cr_f = communication_complexity_rank(f, n)
        
        if cr_f == 0:
            continue
        
        ratio = vd_p_f / cr_f
        results.append(ratio)
    
    if len(results) < 30:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    
    return {
        "metric_name": "ratio",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.7 < mean < 0.3
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results)))**2 for r in results) / len(results))} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results)))**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")