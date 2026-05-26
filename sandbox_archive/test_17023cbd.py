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
    
    # Generate a random Kerdock code with rank r
    n = 30
    r = random.randint(1, 5)
    C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(r)]
    
    # Compute the tropicalization T_C
    T_C = []
    for i in range(n):
        max_val = -math.inf
        for j in range(r):
            if C[j][i] > max_val:
                max_val = C[j][i]
        T_C.append(max_val)
    
    # Compute the minimal rank of T_C
    min_rank_T_C = len(set(T_C))
    
    # Generate a CNF formula F with DPLL search tree width t
    t = random.randint(1, 5)
    F = []
    for _ in range(t):
        clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
        F.append(clause)
    
    # Compute the minimal rank of T_C
    min_rank_T_C = len(set(T_C))
    
    # Check if the conjecture holds
    ratio = min_rank_T_C / (2 ** r)
    std_dev = 3 * math.sqrt(ratio * (1 - ratio) / n)
    conjecture_holds = ratio >= log_2(t) - std_dev and ratio <= log_2(t) + std_dev
    
    return {
        "metric_name": "min_rank_T_C",
        "metric_value": min_rank_T_C,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} not within bounds"
    }

def log_2(x):
    return math.log2(x) if x > 0 else float('-inf')

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")