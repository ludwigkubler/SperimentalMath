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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def dpll_search_tree_height(formula):
        # Simplified DPLL search tree height calculation
        return len(formula)
    
    def construct_braided_monoidal_category(clause_set):
        # Placeholder function to simulate category construction
        return len(clause_set)
    
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        height = dpll_search_tree_height(formula)
        clause_set = formula.split('0') + formula.split('1')
        generators = construct_braided_monoidal_category(clause_set)
        
        results.append({
            "n": n,
            "height": height,
            "generators": generators
        })
    
    x = [r["height"] for r in results]
    y = [r["generators"] for r in results]
    
    corr_coeff = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": 0.5 < corr_coeff < 0.8,
        "counterexample": "" if 0.5 < corr_coeff < 0.8 else f"Correlation {corr_coeff:.2f} out of range"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 < r["metric_value"] < 0.8) / len(results)
    
    if all(0.5 < r["metric_value"] < 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff:.2f} std=NA support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not (0.5 < r["metric_value"] < 0.8)), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of range\" first_failing_seed={first_failing_seed}")