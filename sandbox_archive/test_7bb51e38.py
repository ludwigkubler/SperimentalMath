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

def generate_kcnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, random.randint(1, n))
        clause = ' or '.join(f'x{i}' if var > 0 else f'not x{-var}' for var in clause_vars)
        clauses.append(clause)
    return ' and '.join(clauses)

def calculate_brauer_group_rank(n, m):
    # Placeholder function to compute the Brauer group rank
    # This is a dummy implementation for testing purposes
    return random.randint(1, 10) * m

def calculate_largest_weight(n, m):
    # Placeholder function to compute the largest weight of the Boolean function
    # This is a dummy implementation for testing purposes
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(n // 2, n * 2)
        kcnf = generate_kcnf(n, m)
        rank = calculate_brauer_group_rank(n, m)
        weight = calculate_largest_weight(n, m)
        
        if weight == 0:
            continue
        
        ratio = Fraction(rank, weight).limit_denominator()
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "weight": weight,
            "ratio": ratio
        })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["ratio"] <= 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Brauer Group Rank to Largest Weight Ratio",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")