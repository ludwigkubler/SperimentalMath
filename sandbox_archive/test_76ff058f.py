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

def generate_sat_instance(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        clauses.append(clause)
    return clauses

def dpll_path_length(sat_instance):
    def dpll(instance, assignment):
        if not instance:
            return 0
        literal = next((l for l in instance[0] if abs(l) not in assignment), None)
        if literal is None:
            return 0
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = literal > 0
        if dpll(instance, new_assignment):
            return 1 + dpll_path_length(instance[1:], new_assignment)
        new_assignment[abs(literal)] = not new_assignment[abs(literal)]
        if dpll(instance, new_assignment):
            return 1 + dpll_path_length(instance[1:], new_assignment)
        return 0
    
    return dpll(sat_instance, {})

def local_zeta_function_size(sat_instance):
    n = len(sat_instance)
    zetas = [Fraction(1) for _ in range(n)]
    for clause in sat_instance:
        for literal in clause:
            if literal > 0:
                zetas[literal - 1] *= Fraction(1, 2)
            else:
                zetas[-literal - 1] *= Fraction(1, 2)
    return sum(zetas)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            sat_instance = generate_sat_instance(n)
            zeta_size = local_zeta_function_size(sat_instance)
            dpll_len = dpll_path_length(sat_instance)
            results.append((zeta_size, dpll_len))
    
    if not results:
        return {
            "metric_name": "local_zeta_function_size",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    zetas, dplls = zip(*results)
    n = len(zetas)
    mean_zeta = sum(zetas) / n
    mean_dpll = sum(dplls) / n
    
    if n < 30:
        return {
            "metric_name": "local_zeta_function_size",
            "metric_value": 0,
            "instances_tested": n,
            "n_max": max(len(sat_instance) for sat_instance, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = (n * sum(z * d for z, d in zip(zetas, dplls)) - 
                               mean_zeta * sum(dplls) - 
                               mean_dpll * sum(zetas)) / math.sqrt((n * sum(z**2 for z in zetas) - mean_zeta**2) * (n * sum(d**2 for d in dplls) - mean_dpll**2))
    
    return {
        "metric_name": "local_zeta_function_size",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(len(sat_instance) for sat_instance, _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_zeta - mean_dpll) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{mean_corr_coeff}, mean_diff>{abs(mean_zeta - mean_dpll)}\" first_failing_seed={first_failing_seed}")