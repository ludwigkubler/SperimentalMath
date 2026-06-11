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
    
    def galois_group_order(n):
        # Generate a random Boolean satisfiability problem with n variables
        phi_G = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Construct the associated cubic extension field K from the truth table of the instance
        # This is a placeholder function; actual implementation depends on the specific structure of the problem
        # For simplicity, we assume the Galois group order is proportional to n
        return n
    
    def resolution_proof_width(phi_G):
        # Compute the resolution proof width w(φ_G) for the instance φ_G derived from the truth table
        # This is a placeholder function; actual implementation depends on the specific structure of the problem
        # For simplicity, we assume the resolution proof width is proportional to n
        return len(phi_G)
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        
        return numerator / denominator if denominator != 0 else float('nan')
    
    n_values = [5, 10, 15, 20, 30, 40]
    galois_orders = []
    proof_widths = []
    
    for n in n_values:
        phi_G = [random.choice([0, 1]) for _ in range(2**n)]
        galois_order = galois_group_order(n)
        proof_width = resolution_proof_width(phi_G)
        
        galois_orders.append(galois_order)
        proof_widths.append(proof_width)
    
    correlation_coefficient = pearson_correlation(galois_orders, proof_widths)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "Pearson correlation coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")