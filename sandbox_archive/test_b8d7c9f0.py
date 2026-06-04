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

def binary_form_from_formula(clauses, variables):
    A = [[0] * len(variables) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for j, var in enumerate(clause):
            if var < 0:
                var = ~var
                A[i][variables.index(var)] = -1
            else:
                A[i][variables.index(var)] = 1
    return A

def frobenius_norm(matrix):
    norm = 0
    for row in matrix:
        for val in row:
            norm += val ** 2
    return math.sqrt(norm)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_norm = 0
        total_width = 0
        
        while instances_tested < 30:
            num_vars = random.randint(1, n)
            num_clauses = random.randint(num_vars, min(n * (n - 1) // 2, 2 * num_vars))
            variables = [f'x{i}' for i in range(num_vars)]
            clauses = []
            
            for _ in range(num_clauses):
                clause = random.sample(variables + [-var for var in variables], random.randint(1, num_vars))
                clauses.append(clause)
            
            A = binary_form_from_formula(clauses, variables)
            norm = frobenius_norm(A)
            width = len(clauses)  # Simplified resolution proof width
            
            total_norm += norm
            total_width += width
            instances_tested += 1
        
        avg_norm = total_norm / instances_tested
        avg_width = total_width / instances_tested
        
        results.append({
            "n": n,
            "avg_norm": avg_norm,
            "avg_width": avg_width,
            "instances_tested": instances_tested
        })
    
    correlation_coefficient = 0
    max_norm = -1
    max_width = -1
    
    for result in results:
        correlation_coefficient += (result["avg_norm"] * result["avg_width"])
        if result["avg_norm"] > max_norm:
            max_norm = result["avg_norm"]
        if result["avg_width"] > max_width:
            max_width = result["avg_width"]
    
    correlation_coefficient /= len(results)
    
    conjecture_holds = correlation_coefficient >= 0.8 and max_norm <= 1.5 * max_width
    counterexample = "" if conjecture_holds else f"correlation={correlation_coefficient}, max_norm={max_norm}, max_width={max_width}"
    
    return {
        "metric_name": "Frobenius norm vs Resolution Proof Width",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")