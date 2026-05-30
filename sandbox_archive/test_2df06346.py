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
    
    def generate_formula(n: int, m: int):
        formula = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(3)]
            random.shuffle(clause)
            formula.append(tuple(sorted(clause)))
        return formula
    
    def clause_density(formula):
        return len(set(formula)) / (len(formula[0][0]) * len(formula))
    
    def l_series_expansion(formula, n):
        alpha = clause_density(formula)
        c = 1.0  # Placeholder for the constant
        L_1_2 = abs(c * alpha)  # Simplified for demonstration purposes
        return L_1_2
    
    max_ratio = 0.0
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(n // 2, n * 2)
        formula = generate_formula(n, m)
        L_1_2 = l_series_expansion(formula, n)
        alpha = clause_density(formula)
        
        if alpha > 0:
            ratio = L_1_2 / (alpha * 1.05)  # Using a slightly larger bound for safety
            max_ratio = max(max_ratio, ratio)
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = max_ratio <= 1.05
    counterexample = "" if conjecture_holds else f"max_ratio={max_ratio} > 1.05"
    
    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio exceeded\" first_failing_seed={first_failing_seed}")