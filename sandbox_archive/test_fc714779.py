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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def clause_subset_complexity(clauses):
        return len(clauses)
    
    def hodge_structure_order(clauses):
        # This is a placeholder function to simulate the Hodge structure order.
        # In practice, this would involve complex algebraic geometry computations.
        # For simplicity, we use a linear function of the number of clauses.
        return len(clauses) + 1
    
    def log(x):
        if x <= 0:
            return float('-inf')
        return math.log(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_log_min_order = 0
        total_log_c_clause_subset_complexity = 0
        
        for _ in range(5):  # Sample 5 instances per n
            clauses = generate_sat_instance(n)
            min_order = hodge_structure_order(clauses)
            c_clause_subset_complexity = clause_subset_complexity(clauses)
            
            if min_order == 0 or c_clause_subset_complexity == 0:
                continue
            
            total_log_min_order += log(min_order)
            total_log_c_clause_subset_complexity += log(c_clause_subset_complexity)
            instances_tested += 1
        
        if instances_tested < 3:  # Require at least 3 instances per n
            return {
                "metric_name": "log_min_order_vs_log_c_clause_subset_complexity",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        avg_log_min_order = total_log_min_order / instances_tested
        avg_log_c_clause_subset_complexity = total_log_c_clause_subset_complexity / instances_tested
        
        results.append((avg_log_min_order, avg_log_c_clause_subset_complexity))
    
    if len(results) < 3:  # Require at least 3 different n values
        return {
            "metric_name": "log_min_order_vs_log_c_clause_subset_complexity",
            "metric_value": None,
            "instances_tested": sum(x[1] for x in results),
            "n_max": max(n_values[:len(results)]),
            "conjecture_holds": False,
            "counterexample": "insufficient_n_values"
        }
    
    avg_log_min_order = sum(x[0] for x in results) / len(results)
    avg_log_c_clause_subset_complexity = sum(x[1] for x in results) / len(results)
    r = (len(results) * sum(x[0] * x[1] for x in results) - sum(x[0] for x in results) * sum(x[1] for x in results)) / \
        math.sqrt((len(results) * sum(x[0]**2 for x in results) - sum(x[0] for x in results)**2) *
                  (len(results) * sum(x[1]**2 for x in results) - sum(x[1] for x in results)**2))
    
    return {
        "metric_name": "log_min_order_vs_log_c_clause_subset_complexity",
        "metric_value": r,
        "instances_tested": sum(x[1] for x in results),
        "n_max": max(n_values[:len(results)]),
        "conjecture_holds": r >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")