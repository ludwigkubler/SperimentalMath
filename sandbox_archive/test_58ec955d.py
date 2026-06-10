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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def circuit_satisfiability_complexity(cnf):
        # Simplified complexity measure based on number of clauses
        return len(cnf)
    
    def geometric_quantization_rank(cnf):
        # Simplified rank measure based on number of variables
        n = max(abs(x) for clause in cnf for x in clause)
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            gqr = geometric_quantization_rank(cnf)
            cssc = circuit_satisfiability_complexity(cnf)
            results.append({"n": n, "gqr": gqr, "cssc": cssc})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    gqr_values = [result["gqr"] for result in results]
    cssc_values = [result["cssc"] for result in results]
    
    mean_gqr = sum(gqr_values) / len(gqr_values)
    mean_cssc = sum(cssc_values) / len(cssc_values)
    
    covariance = sum((x - mean_gqr) * (y - mean_cssc) for x, y in zip(gqr_values, cssc_values))
    variance_gqr = sum((x - mean_gqr) ** 2 for x in gqr_values)
    variance_cssc = sum((y - mean_cssc) ** 2 for y in cssc_values)
    
    if variance_gqr == 0 or variance_cssc == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_gqr) * math.sqrt(variance_cssc))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.7,
        "counterexample": ""
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
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")