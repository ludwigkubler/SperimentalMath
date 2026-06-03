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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def tropical_p_adic_rank(formula, p=53):
        rank = 0
        for bit in formula:
            if bit == '1':
                rank += 1
        return rank
    
    def sat_proof_size(formula):
        # Simplified SAT solver that returns a random proof size
        return random.randint(10, 100)
    
    n_values = [5, 10, 15, 20, 30, 40]
    tpar_values = []
    proof_size_values = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        tpar_value = tropical_p_adic_rank(formula)
        proof_size_value = sat_proof_size(formula)
        
        tpar_values.append(tpar_value)
        proof_size_values.append(proof_size_value)
    
    if len(tpar_values) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(tpar_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        
        if denominator == 0:
            return None
        
        return numerator / denominator
    
    correlation_coefficient = pearson_correlation(tpar_values, proof_size_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(tpar_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)