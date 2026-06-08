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

def generate_random_sat_instance(n, d):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(d):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def truth_table_to_diophantine(clauses):
    n = len(clauses[0])
    binary = [0] * (2 ** n)
    for i in range(1, 2 ** n):
        binary[i] = bin(i)[2:].zfill(n)
        if all(binary[j-1] == '1' or c * int(binary[abs(c)-1]) >= 0 for c in clauses):
            return len(binary) - 1
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_diff = 0
        
        for _ in range(30):
            d = random.randint(1, n)
            clauses = generate_random_sat_instance(n, d)
            diophantine_exponent = truth_table_to_diophantine(clauses)
            
            if diophantine_exponent is not None:
                instances_tested += 1
                diff = abs(diophantine_exponent - math.log(n) ** 2 * d)
                total_diff += diff
        
        if instances_tested == 0:
            continue
        
        mean_diff = total_diff / instances_tested
        conjecture_holds = mean_diff <= 3
        counterexample = "" if conjecture_holds else f"n={n}, diophantine_exponent={diophantine_exponent}, expected={math.log(n) ** 2 * d}"
        
        results.append({
            "metric_name": "minimal_diophantine_exponent",
            "metric_value": diophantine_exponent,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    if not results:
        return {
            "seed": seed,
            "metric_name": "minimal_diophantine_exponent",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean": mean_value,
        "std": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "mean" in trial_result and "std" in trial_result and "support_fraction" in trial_result:
            results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
    else:
        mean_value = sum(result["mean"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["mean"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")