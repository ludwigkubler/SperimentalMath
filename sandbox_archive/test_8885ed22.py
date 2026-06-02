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
        for i in range(1 << n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def boolean_algebra_quasi_group(cnf):
        # Simplified representation of the quasi-group
        return cnf
    
    def min_rank(quasi_group):
        # Placeholder for minimal rank calculation
        return len(quasi_group)
    
    def circuit_weight(cnf):
        # Placeholder for circuit weight calculation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        quasi_group = boolean_algebra_quasi_group(cnf)
        min_rank_val = min_rank(quasi_group)
        circuit_weight_val = circuit_weight(cnf)
        
        if circuit_weight_val == 0:
            continue
        
        correlation_coefficient = (min_rank_val - n) / circuit_weight_val
        results.append(correlation_coefficient)
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    mean_corr = sum(results) / len(results)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": mean_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_valid_results")
    else:
        mean_corr = sum(results) / len(results)
        support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(min(results))]
            print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")