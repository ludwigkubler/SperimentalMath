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
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice(['', 'not ']) + random.choice([f'x{i}' for i in range(1, n+1)]) for _ in range(3)]
            clause = f"({' or '.join(literals)})"
            clauses.append(clause)
        return f"({' and '.join(clauses)})"
    
    def count_clauses(formula):
        return formula.count(' and ')
    
    def coherence_length(n):
        # Placeholder implementation for coherence length
        # This is a dummy function that returns a random value between 1 and n
        return random.randint(1, n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        kappa = count_clauses(formula)
        c = coherence_length(n)
        results.append((c, kappa))
    
    if len(results) < 30:
        return {
            "metric_name": "coherence_length",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([n for _, n in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    c_values = [c for c, _ in results]
    kappa_values = [kappa for _, kappa in results]
    
    mean_c = sum(c_values) / len(c_values)
    mean_kappa = sum(kappa_values) / len(kappa_values)
    
    slope = (sum((c - mean_c) * (kappa - mean_kappa) for c, kappa in results) /
             sum((kappa - mean_kappa)**2 for kappa in kappa_values))
    
    if slope < 0.8 or abs(mean_c - mean_kappa) > 3:
        return {
            "metric_name": "coherence_length",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([n for _, n in results]),
            "conjecture_holds": False,
            "counterexample": f"insufficient_correlation (slope={slope}, mean_diff={abs(mean_c - mean_kappa)})"
        }
    
    return {
        "metric_name": "coherence_length",
        "metric_value": slope,
        "instances_tested": len(results),
        "n_max": max([n for _, n in results]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_slope = sum(result["metric_value"] for result in results) / len(results)
        std_slope = math.sqrt(sum((result["metric_value"] - mean_slope)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")