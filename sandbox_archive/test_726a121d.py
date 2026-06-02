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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frege_proof_length(cnf):
        # Simplified Frege proof length calculation
        return len(cnf) * 2
    
    def quaternionic_kahler_form(cnf):
        # Simplified mapping of CNF to quaternionic Kähler form order
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        qkf_order = quaternionic_kahler_form(cnf)
        proof_length = frege_proof_length(cnf)
        
        if qkf_order == 0 or proof_length == 0:
            continue
        
        log_qkf_order = math.log(qkf_order)
        log_n_fact = math.log(math.factorial(n))
        log_phi = math.log(proof_length)
        
        correlation_coefficient = (log_qkf_order - log_n_fact * log_phi) / qkf_order
        results.append({
            "n": n,
            "m": m,
            "qkf_order": qkf_order,
            "proof_length": proof_length,
            "correlation_coefficient": correlation_coefficient
        })
    
    if not results:
        return {
            "metric_name": "logarithmic_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_corr_coeff = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_corr_coeff = math.sqrt(sum((result["correlation_coefficient"] - mean_corr_coeff) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "logarithmic_correlation",
        "metric_value": mean_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_corr_coeff >= 0.8 and all(abs(result["correlation_coefficient"]) <= 3 * std_corr_coeff for result in results),
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
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data n_tested={len(results)}")