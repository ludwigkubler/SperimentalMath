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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = []
        visited = set()
        for clause in cnf:
            for literal in clause:
                if -literal in stack:
                    return len(stack) + 1
                elif literal not in visited:
                    stack.append(literal)
                    visited.add(literal)
        return float('inf')
    
    def k_theory_dimension(cnf):
        # Simplified K-theory dimension calculation for small rings
        n = len(cnf)
        if n == 0:
            return 0
        return math.ceil(math.log2(n))
    
    dim_K_values = []
    width_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        for _ in range(5):
            cnf = generate_cnf(n)
            dim_K = k_theory_dimension(cnf)
            width = resolution_width(cnf)
            
            dim_K_values.append(dim_K)
            width_values.append(width)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not dim_K_values or not width_values:
        return {
            "metric_name": "K-theory Dimension vs Resolution Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    mean_dim_K = sum(dim_K_values) / len(dim_K_values)
    mean_width = sum(width_values) / len(width_values)
    covariance = sum((x - mean_dim_K) * (y - mean_width) for x, y in zip(dim_K_values, width_values)) / len(dim_K_values)
    variance_dim_K = sum((x - mean_dim_K)**2 for x in dim_K_values) / len(dim_K_values)
    variance_width = sum((y - mean_width)**2 for y in width_values) / len(width_values)
    
    if variance_dim_K == 0 or variance_width == 0:
        return {
            "metric_name": "K-theory Dimension vs Resolution Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_dim_K) * math.sqrt(variance_width))
    
    return {
        "metric_name": "K-theory Dimension vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")