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
    
    # Define the function f in P (for simplicity, let's use a polynomial over GF(p))
    p = 7  # A prime number for p-adic analysis
    n = 10  # Degree of the polynomial
    coefficients = [random.randint(0, p-1) for _ in range(n+1)]
    
    # Compute the p-adic Fourier series and its minimal rank
    def p_adic_fourier_series(f, x):
        result = 0
        for i in range(len(f)):
            result += f[i] * (x ** i)
        return result
    
    min_rank = float('inf')
    for x in range(p):
        fourier_value = p_adic_fourier_series(coefficients, x)
        rank = len(set([fourier_value % p]))
        if rank < min_rank:
            min_rank = rank
    
    # Construct the DPLL search tree and measure its width
    def dpll_tree_width(formula):
        # Simplified version of DPLL algorithm to estimate width
        if not formula:
            return 1
        subformula = formula[0]
        if 'or' in subformula:
            left, right = subformula.split(' or ')
            return max(dpll_tree_width(left), dpll_tree_width(right))
        elif 'and' in subformula:
            left, right = subformula.split(' and ')
            return dpll_tree_width(left) + dpll_tree_width(right)
        else:
            return 1
    
    formula = "x1 or x2 and x3"
    width = dpll_tree_width(formula)
    
    # Calculate the logarithm of the width of the DPLL search tree
    log_width = math.log(width, p) if width > 0 else 0
    
    # Compare the minimal rank with the logarithm of the DPLL tree width
    ratio = log_width / min_rank if min_rank > 0 else float('inf')
    
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8 and abs(log_width - min_rank) <= 3,
        "counterexample": "" if ratio >= 0.8 and abs(log_width - min_rank) <= 3 else "Ratio out of bounds"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    ratios = []
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            support_count += 1
        ratios.append(trial_result["metric_value"])
    
    mean_ratio = sum(ratios) / len(ratios)
    std_deviation = math.sqrt(sum((r - mean_ratio) ** 2 for r in ratios)) / len(ratios)
    support_fraction = support_count / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(trial_result["counterexample"] for trial_result in run_trial(seed) for seed in seeds):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")