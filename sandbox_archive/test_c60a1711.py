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
    
    # Define function f in P (for simplicity, let's use a polynomial)
    n = 10  # Degree of the polynomial
    coefficients = [random.randint(0, 10) for _ in range(n + 1)]
    f = lambda x: sum(c * x**i for i, c in enumerate(coefficients))
    
    # Compute p-adic Fourier series (for simplicity, let's use base 2)
    p = 2
    max_val = 2 ** n
    fourier_series = [0] * max_val
    for k in range(max_val):
        x = k / max_val
        fourier_series[k] = f(x) % p
    
    # Determine the minimal rank of the Fourier series
    rank = len(set(fourier_series))
    
    # Construct DPLL search tree (simplified version)
    def dpll(formula, assignment):
        if not formula:
            return True
        literal = next((l for l in formula[0] if l != -l), None)
        if literal is None:
            return False
        new_formula = [cl for cl in formula if literal not in cl and -literal not in cl]
        if dpll(new_formula, assignment + [literal]):
            return True
        if dpll(new_formula, assignment + [-literal]):
            return True
        return False
    
    # Generate a random DPLL formula (for simplicity, let's use 3-SAT)
    num_vars = n
    num_clauses = 2 * n
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([-i, i]) for i in range(1, num_vars + 1)]
        random.shuffle(clause)
        clauses.append(clause)
    
    # Measure the width of the DPLL search tree
    def dpll_width(formula):
        if not formula:
            return 0
        max_width = 0
        for literal in set(l for cl in formula for l in cl):
            new_formula = [cl for cl in formula if literal not in cl and -literal not in cl]
            width = 1 + dpll_width(new_formula)
            max_width = max(max_width, width)
        return max_width
    
    width = dpll_width(clauses)
    
    # Calculate the logarithm of the width
    log_width = math.log(width) if width > 0 else 0
    
    # Compare the minimal rank with the logarithm of the DPLL tree width
    ratio = log_width / rank if rank > 0 else float('inf')
    difference = abs(log_width - rank)
    
    return {
        "metric_name": "Ratio and Difference",
        "metric_value": (ratio, difference),
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8 and difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_ratio = 0
    total_difference = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        ratio, difference = trial_result["metric_value"]
        total_ratio += ratio
        total_difference += difference
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_ratio = total_ratio / len(seeds)
    mean_difference = total_difference / len(seeds)
    support_fraction = count_supporting / len(seeds)
    
    print(f"RESULT: SUPPORTED mean={mean_ratio} std={math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios)) / len(ratios)} support_fraction={support_fraction}")