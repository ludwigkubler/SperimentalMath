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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(x != 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_proof_width(clauses):
        # Simplified version of resolution proof width calculation
        return len(set(tuple(sorted(c)) for c in clauses))
    
    def geometric_entropy(clauses):
        n = len(clauses[0])
        entropy = 0
        for clause in clauses:
            prob = Fraction(1, 2**n)
            entropy += -prob * math.log2(prob)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_proof_width(cnf)
        entropy = geometric_entropy(cnf)
        results.append((n, width, entropy))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _ in results)
    instances_tested = len(results)
    
    # Calculate correlation coefficient
    x_mean = sum(width for _, width, _ in results) / instances_tested
    y_mean = sum(entropy for _, _, entropy in results) / instances_tested
    numerator = sum((width - x_mean) * (entropy - y_mean) for _, width, entropy in results)
    denominator = math.sqrt(sum((width - x_mean)**2 for _, width, _ in results)) * math.sqrt(sum((entropy - y_mean)**2 for _, _, entropy in results))
    
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient is not None and correlation_coefficient > 0.95
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")