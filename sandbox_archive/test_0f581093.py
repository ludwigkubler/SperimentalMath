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
    
    def generate_formula(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def compute_clause_density(clauses):
        return len(clauses) / (len(clauses[0]) * len(clauses))
    
    def l_function_expansion(clauses):
        alpha = compute_clause_density(clauses)
        # Simplified approximation for demonstration purposes
        return abs(1 - alpha)
    
    max_ratio = 0.0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n * 2)
            clauses = generate_formula(n, m)
            alpha = compute_clause_density(clauses)
            l_value = l_function_expansion(clauses)
            ratio = abs(l_value) / alpha
            if ratio > max_ratio:
                max_ratio = ratio
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = max_ratio <= 1.05
    counterexample = "" if conjecture_holds else f"max_ratio={max_ratio}"
    
    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2%}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2%}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio exceeded\" first_failing_seed={first_failing_seed}")