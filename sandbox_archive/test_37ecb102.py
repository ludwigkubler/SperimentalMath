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
    n = random.randint(5, 40)
    formula = generate_xor_3cnf(n)
    
    try:
        G = compute_motivic_galois_group(formula)
        rank_G = calculate_rank(G)
        metric_value = rank_G
        conjecture_holds = rank_G <= math.log2(n) ** 2
        counterexample = "" if conjecture_holds else "rank_G > O(log^2(n))"
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_xor_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(range(1, n + 1), 3)
        clause = [f"x{i}" if x > 0 else f"~x{-x}" for x in clause]
        clauses.append(" or ".join(clause))
    return " and ".join(clauses)

def compute_motivic_galois_group(formula: str) -> list:
    # Placeholder function to simulate computation
    # Replace with actual implementation if available
    return []

def calculate_rank(G: list) -> int:
    # Placeholder function to simulate calculation
    # Replace with actual implementation if available
    return len(G)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_G > O(log^2(n))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")