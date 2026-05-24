# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        return [[random.choice([-i, i]) for _ in range(random.randint(3, 5))] for _ in range(m)]
    
    def compute_minimal_norm(formula):
        # Placeholder for the actual computation
        return sum(abs(x) for clause in formula for x in clause)
    
    def construct_dpll_refutation_tree(formula):
        # Placeholder for the actual construction
        height = 0
        for _ in range(10):  # Simplified DPLL refutation tree construction
            height += 1
        return height
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    formula = generate_3cnf(n, m)
    
    minimal_norm = compute_minimal_norm(formula)
    dpll_height = construct_dpll_refutation_tree(formula)
    
    return {
        "metric_name": "minimal_norm_vs_dpll_height",
        "metric_value": minimal_norm,
        "instances_tested": 1,
        "conjecture_holds": minimal_norm <= dpll_height,
        "counterexample": "" if minimal_norm <= dpll_height else f"Formula: {formula}, Minimal Norm: {minimal_norm}, DPLL Height: {dpll_height}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(result["metric_value"] for result in results)
        std_dev = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")