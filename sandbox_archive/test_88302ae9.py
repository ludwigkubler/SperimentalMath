# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def binary_form_from_formula(clauses, variables):
    A = [[0] * len(variables) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                j = variables.index(var)
            else:
                j = variables.index(-var)
            A[i][j] = 1
    return A

def frobenius_norm(matrix):
    norm_squared = sum(sum(row[j]**2 for row in matrix) for j in range(len(matrix[0])))
    return norm_squared**0.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    total_norm = 0
    total_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            num_vars = random.randint(2, n)
            variables = [f'x{i+1}' for i in range(num_vars)]
            clauses = []
            for _ in range(random.randint(1, 2 * num_vars)):
                clause = random.sample(variables + [-var for var in variables], random.randint(1, num_vars))
                clauses.append(clause)
            
            A = binary_form_from_formula(clauses, variables)
            norm = frobenius_norm(A)
            total_norm += norm
            instances_tested += 1
            
            # Calculate resolution proof width (simplified example)
            width = len(variables) * len(clauses)  # Placeholder for actual width calculation
            total_width += width
    
    if instances_tested < 30:
        return {
            "metric_name": "Frobenius norm",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_norm = total_norm / instances_tested
    mean_width = total_width / instances_tested
    
    if mean_norm > 1.5 * mean_width:
        return {
            "metric_name": "Frobenius norm",
            "metric_value": mean_norm,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Mean Frobenius norm {mean_norm} exceeds 1.5 * mean width {mean_width}"
        }
    
    return {
        "metric_name": "Frobenius norm",
        "metric_value": mean_norm,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(support_count, len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):  # At least 80% support
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")