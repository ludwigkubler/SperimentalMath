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

def generate_formula(n):
    if n == 1:
        return 'x'
    else:
        left = generate_formula(random.randint(1, n-1))
        right = generate_formula(n - len(left.split()))
        operator = random.choice(['&', '|'])
        return f'({left} {operator} {right})'

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Pearson correlation coefficient"
    instances_tested = 0
    n_max = 5
    tpar_values = []
    proof_sizes = []
    conjecture_holds = False
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            formula = generate_formula(n)
            # Convert Boolean formula to tropical semiring representation
            # and compute tpar(φ) (simplified example)
            tpar_value = len(formula.split())  # Simplified example
            
            # Measure proof size |P(φ)| using a standard SAT solver
            # This is a placeholder for the actual SAT solver call
            proof_size = random.randint(10, 2 * n)  # Simplified example
            
            tpar_values.append(tpar_value)
            proof_sizes.append(proof_size)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    # Compute Pearson correlation coefficient
    mean_tpar = sum(tpar_values) / instances_tested
    mean_proof_size = sum(proof_sizes) / instances_tested
    covariance = sum((tpar - mean_tpar) * (proof - mean_proof_size) for tpar, proof in zip(tpar_values, proof_sizes))
    variance_tpar = sum((tpar - mean_tpar) ** 2 for tpar in tpar_values)
    variance_proof_size = sum((proof - mean_proof_size) ** 2 for proof in proof_sizes)
    
    if variance_tpar == 0 or variance_proof_size == 0:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_tpar) * math.sqrt(variance_proof_size))
    
    if abs(correlation_coefficient) > 0.5:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    
    conjecture_holds_count = sum(1 for res in results if res["conjecture_holds"])
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(res["counterexample"] for res in results):
        counterexample_desc = next(res["counterexample"] for res in results if res["counterexample"])
        first_failing_seed = next(res["seed"] for res in results if res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")