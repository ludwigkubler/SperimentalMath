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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} OR {~var}')
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append(f'{variables[i-1]} AND {variables[j-1]} OR ~{variables[i-1]} OR ~{variables[j-1]}')
        return f'NOT ({" AND ".join(clauses)})'
    
    def hodge_structure(formula):
        # Placeholder for Hodge structure computation
        # This is a dummy implementation and should be replaced with actual code
        return random.random()
    
    def frege_proof_depth(formula):
        # Placeholder for Frege proof depth computation
        # This is a dummy implementation and should be replaced with actual code
        return len(formula.split())
    
    n = 10  # Example value, replace with actual range
    results = []
    for _ in range(30):
        formula = generate_tseitin_formula(n)
        lid = hodge_structure(formula)
        f_phi = frege_proof_depth(formula)
        results.append((lid, f_phi))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    lid_values = [r[0] for r in results]
    f_phi_values = [r[1] for r in results]
    mean_lid = sum(lid_values) / len(lid_values)
    mean_f_phi = sum(f_phi_values) / len(f_phi_values)
    covariance = sum((lid - mean_lid) * (f_phi - mean_f_phi) for lid, f_phi in results) / len(results)
    variance_lid = sum((lid - mean_lid) ** 2 for lid in lid_values) / len(lid_values)
    variance_f_phi = sum((f_phi - mean_f_phi) ** 2 for f_phi in f_phi_values) / len(f_phi_values)
    correlation_coefficient = covariance / (math.sqrt(variance_lid) * math.sqrt(variance_f_phi))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")