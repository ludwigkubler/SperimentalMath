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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_path_length(clauses):
        stack = [(clauses, 0)]
        path_length = 0
        while stack:
            clauses, i = stack.pop()
            if not clauses:
                continue
            literal = clauses[0][i]
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            stack.append((new_clauses, (i + 1) % len(clauses)))
            path_length += 1
        return path_length
    
    def local_zeta_function_size(clauses):
        size = 0
        for clause in clauses:
            size += len(clause)
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_zeta_size = 0
        total_path_length = 0
        
        while len(results) < 30 or (len(results) >= 30 and not all(r['conjecture_holds'] for r in results)):
            clauses = generate_sat_instance(n)
            zeta_size = local_zeta_function_size(clauses)
            path_length = dpll_path_length(clauses)
            
            instances_tested += 1
            total_zeta_size += zeta_size
            total_path_length += path_length
            
            if len(results) < 30:
                results.append({
                    "metric_name": "zeta_size",
                    "metric_value": zeta_size,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": True,
                    "counterexample": ""
                })
            else:
                mean_zeta = total_zeta_size / len(results)
                mean_path = total_path_length / len(results)
                correlation = sum((r['metric_value'] - mean_zeta) * (mean_path - mean_path) for r in results) / len(results)
                abs_diff = sum(abs(r['metric_value'] - mean_path) for r in results) / len(results)
                
                if correlation >= 0.8 and abs_diff <= 3:
                    results[-1]['conjecture_holds'] = True
                else:
                    results[-1]['conjecture_holds'] = False
                    results[-1]['counterexample'] = "correlation_threshold_not_met"
                    
        if len(results) >= 30 and not all(r['conjecture_holds'] for r in results):
            return {
                "seed": seed,
                "metric_name": "zeta_size",
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "correlation_threshold_not_met"
            }
    
    mean_zeta = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_zeta) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "zeta_size",
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_zeta = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_zeta) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_zeta} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_zeta} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_threshold_not_met' first_failing_seed={first_failing_seed}")