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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def dpll_path_length(clauses):
        stack = [(clauses, [])]
        while stack:
            clauses, path = stack.pop()
            if not clauses:
                return len(path)
            literal = next(lit for lit in range(1, len(clauses) + 1) if any(lit in clause or -lit in clause for clause in clauses))
            new_clauses = [clause for clause in clauses if literal not in clause and -literal not in clause]
            stack.append((new_clauses, path + [(literal, 'F')]))
            stack.append(([c for c in new_clauses if any(-lit in c for lit in c)], path + [(literal, 'T')]))
        return float('inf')

    def local_zeta_function_size(clauses):
        # Placeholder algorithm: compute zeta function at each variable
        size = 0
        for clause in clauses:
            size += len(set(abs(lit) for lit in clause))
        return size

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_zeta_size = 0
        total_dpll_path_length = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            zeta_size = local_zeta_function_size(clauses)
            dpll_len = dpll_path_length(clauses)
            
            if zeta_size > 0 and dpll_len != float('inf'):
                total_zeta_size += zeta_size
                total_dpll_path_length += dpll_len
                instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        mean_zeta = total_zeta_size / instances_tested
        mean_dpll = total_dpll_path_length / instances_tested
        correlation_coefficient = (instances_tested * sum(zeta * dpll for zeta, dpll in zip(results, results)) - 
                                   sum(results) * sum(results)) / math.sqrt((instances_tested * sum(zeta**2 for zeta in results) - sum(results)**2) *
                                                                 (instances_tested * sum(dpll**2 for dpll in results) - sum(results)**2))
        mean_abs_diff = sum(abs(zeta - dpll) for zeta, dpll in zip(results, results)) / instances_tested
        
        if correlation_coefficient >= 0.8 and mean_abs_diff <= 3:
            conjecture_holds = True
        else:
            conjecture_holds = False
        
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": conjecture_holds,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8 and abs(r - mean_value) <= 3) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.8 or abs(r - mean_value) > 3 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < 0.8 or abs(r - mean_value) > 3))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")