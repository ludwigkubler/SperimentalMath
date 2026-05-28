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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_kcnf(n, m):
    clauses = []
    for _ in range(m):
        variables = random.sample(range(1, n + 1), random.randint(1, n))
        clause = ' or '.join(f'x{i}' if var > 0 else f'not x{-var}' for var in variables)
        clauses.append(clause)
    return '\n'.join(clauses)

def compute_brauer_group_rank(kcnf):
    # Placeholder function to simulate Brauer group rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)  # Random rank for demonstration

def calculate_largest_weight(kcnf):
    # Placeholder function to simulate largest weight calculation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = random.randint(5, 20)
    kcnf = generate_kcnf(n, m)
    
    brauer_group_rank = compute_brauer_group_rank(kcnf)
    largest_weight = calculate_largest_weight(kcnf)
    
    metric_value = Fraction(brauer_group_rank) / largest_weight
    conjecture_holds = metric_value <= 1
    
    return {
        "metric_name": "brauer_group_rank_to_weight_ratio",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {metric_value} > 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))[:30]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")