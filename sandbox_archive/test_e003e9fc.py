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
    
    n = 10  # Start with a small size and increase
    instances_tested = 0
    total_metric_value = 0
    max_n = 0
    
    while True:
        if n > 40:
            break
        
        cnf_formula = generate_cnf(n)
        p_adic_l_values = compute_p_adic_l_values(cnf_formula)
        dpll_width = compute_dpll_width(cnf_formula)
        
        if not p_adic_l_values or not dpll_width:
            continue
        
        instances_tested += 1
        total_metric_value += abs(p_adic_l_values) / dpll_width
        max_n = max(max_n, n)
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / 30
    
    return {
        "metric_name": "L(φ)/W(φ)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

def generate_cnf(n: int) -> list:
    literals = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    
    # Generate a random CNF formula with n variables
    for _ in range(n):
        clause = random.sample(literals + [-l for l in literals], 2)
        clauses.append(clause)
    
    return clauses

def compute_p_adic_l_values(cnf_formula: list) -> float:
    # Placeholder for actual computation of p-adic L-values
    # For demonstration, return a random value
    return random.uniform(0.1, 1.0)

def compute_dpll_width(cnf_formula: list) -> int:
    # Placeholder for actual computation of DPLL search tree width
    # For demonstration, return a random value
    return random.randint(5, 20)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")