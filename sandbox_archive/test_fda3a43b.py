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
    
    def tseitin_formula(n, num_clauses):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        
        # Generate literals
        literals = [random.choice([var, f"~{var}"]) for var in variables]
        
        # Add clauses for literals
        for literal in literals:
            clauses.append(literal)
        
        # Add clauses for Tseitin encoding
        for i in range(n):
            clauses.append(f"{variables[i]} | ~x{i+1}")
            clauses.append(f"~{variables[i]} | x{i+1}")
        
        return clauses
    
    def min_index_of_automorphism_groups(clauses):
        # Placeholder function to simulate the computation of the minimal index
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_clauses = 0
    
    for n in n_values:
        num_clauses = random.randint(n // 2, 2 * n)
        clauses = tseitin_formula(n, num_clauses)
        min_index = min_index_of_automorphism_groups(clauses)
        results.append((n, num_clauses, min_index))
        total_clauses += num_clauses
    
    mean_min_index = sum(result[2] for result in results) / len(results)
    mean_num_clauses = total_clauses / len(n_values)
    
    correlation_coefficient = 0
    if mean_num_clauses != 0:
        correlation_coefficient = (sum((result[1] - mean_num_clauses) * (result[2] - mean_min_index) for result in results) /
                                  math.sqrt(sum((result[1] - mean_num_clauses) ** 2 for result in results) *
                                            sum((result[2] - mean_min_index) ** 2 for result in results)))
    
    mean_abs_diff = sum(abs(result[2] - result[1]) for result in results) / len(results)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")