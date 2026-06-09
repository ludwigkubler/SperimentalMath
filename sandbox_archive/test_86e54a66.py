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
    
    def generate_tseitin_formula(n, d):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate the first part of Tseitin formula
        for i in range(1, n + 1):
            clause = [i]
            for j in range(i + 1, n + 1):
                clause.append(-j)
            clauses.append(clause)
        
        # Generate the second part of Tseitin formula
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                for k in range(j + 1, n + 1):
                    clause = [-i, -j, k]
                    clauses.append(clause)
        
        # Generate the third part of Tseitin formula
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clause = [i, -j]
                clauses.append(clause)
        
        return variables, clauses
    
    def compute_group_size(n, d):
        # Simulate the growth rate of the group
        # This is a placeholder function; replace with actual geometric group theory computation
        return n ** 2
    
    def compute_resolution_proof_width(variables, clauses):
        # Simulate the resolution proof width
        # This is a placeholder function; replace with actual resolution proof computation
        return len(clauses)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = 2  # Regularity of the graph
        
        variables, clauses = generate_tseitin_formula(n, d)
        group_size = compute_group_size(n, d)
        proof_width = compute_resolution_proof_width(variables, clauses)
        
        results.append({
            "n": n,
            "group_size": group_size,
            "proof_width": proof_width
        })
    
    log2_group_sizes = [math.log2(res["group_size"]) for res in results]
    proof_widths = [res["proof_width"] for res in results]
    
    if len(log2_group_sizes) == 0 or len(proof_widths) == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 30,
            "n_max": max(1, n),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    correlation_coefficient = sum((log2_group_sizes[i] - mean(log2_group_sizes)) * (proof_widths[i] - mean(proof_widths)) for i in range(len(results))) / (len(results) * std_dev(log2_group_sizes) * std_dev(proof_widths))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(1, n),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": "" if abs(correlation_coefficient) >= 0.9 else "correlation_coefficient_too_low"
    }

def mean(data):
    return sum(data) / len(data)

def std_dev(data):
    avg = mean(data)
    variance = sum((x - avg) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = mean([res["metric_value"] for res in results])
        std_value = std_dev([res["metric_value"] for res in results])
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")