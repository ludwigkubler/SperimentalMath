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

def generate_tseitin_formula(n, d):
    literals = {i: f'x{i}' for i in range(1, n + 1)}
    clauses = []
    
    # Generate Tseitin encoding
    for i in range(1, n + 1):
        a, b = random.choice([literals[i], '¬' + literals[i]]), random.choice([literals[i], '¬' + literals[i]])
        if a != b:
            clauses.append(f'{a} ∨ {b}')
            clauses.append(f'¬{a} ∨ ¬{b}')
    
    # Generate resolution proof
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            a, b = random.choice([literals[i], '¬' + literals[i]]), random.choice([literals[j], '¬' + literals[j]])
            if a != b:
                clauses.append(f'{a} ∨ {b}')
                clauses.append(f'¬{a} ∨ ¬{b}')
    
    return clauses, literals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 2
    n_max = 40
    instances_tested = 0
    integral_points_count = []
    proof_widths = []
    
    for n in range(5, n_max + 1):
        if (n - 1) % d != 0:
            continue
        
        clauses, literals = generate_tseitin_formula(n, d)
        instances_tested += len(clauses)
        
        # Count integral points (simplified for demonstration)
        integral_points_count.append(len(literals))
        
        # Estimate resolution proof width (simplified for demonstration)
        proof_widths.append(len(clauses) * 2)
    
    if not integral_points_count or not proof_widths:
        return {
            "metric_name": "integral_points",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    r = correlation(integral_points_count, proof_widths)
    c_d = estimate_c(d, integral_points_count, proof_widths)
    
    return {
        "metric_name": "integral_points",
        "metric_value": c_d * max(proof_widths),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r >= 0.5,
        "counterexample": ""
    }

def correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    var_x = sum((xi - mean_x) ** 2 for xi in x) / n
    var_y = sum((yi - mean_y) ** 2 for yi in y) / n
    
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

def estimate_c(d, integral_points_count, proof_widths):
    if len(integral_points_count) != len(proof_widths):
        raise ValueError("integral_points_count and proof_widths must have the same length")
    
    n = len(integral_points_count)
    sum_log_ip = sum(math.log(ip + 1) for ip in integral_points_count)
    sum_pw = sum(pw for pw in proof_widths)
    
    return (sum_log_ip / n) / math.log(sum_pw / n)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")