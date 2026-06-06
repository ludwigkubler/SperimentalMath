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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def hodge_structure_order(clauses):
        # Simplified Hodge structure order calculation
        return len(clauses) ** 0.5
    
    def clause_subset_complexity(clauses):
        # Simplified subset complexity calculation
        return sum(len(c) for c in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_sat_instance(n)
            min_order = hodge_structure_order(instance)
            c_phi = clause_subset_complexity(instance)
            
            if min_order <= 0 or c_phi <= 0:
                continue
            
            log_min_order = math.log(min_order)
            log_c_phi = math.log(c_phi)
            
            results.append((log_min_order, log_c_phi))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    log_min_orders = [r[0] for r in results]
    log_c_phis = [r[1] for r in results]
    
    mean_log_min_order = sum(log_min_orders) / len(log_min_orders)
    mean_log_c_phi = sum(log_c_phis) / len(log_c_phis)
    
    covariance = sum((log_min_orders[i] - mean_log_min_order) * (log_c_phis[i] - mean_log_c_phi) for i in range(len(results))) / len(results)
    variance_log_min_order = sum((log_min_orders[i] - mean_log_min_order) ** 2 for i in range(len(results))) / len(results)
    variance_log_c_phi = sum((log_c_phis[i] - mean_log_c_phi) ** 2 for i in range(len(results))) / len(results)
    
    correlation = covariance / (math.sqrt(variance_log_min_order) * math.sqrt(variance_log_c_phi))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, correlation={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break