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
    
    def generate_random_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def boolean_tensor_product_width(clauses):
        width = 0
        for clause in clauses:
            width |= sum(abs(x) for x in clause)
        return width
    
    def min_rank_tqft(clauses):
        # Placeholder function to simulate TQFT computation
        # Actual implementation would depend on the specific TQFT construction
        rank = len(clauses) * 2  # Simplified example
        return rank
    
    n = random.randint(5, 40)
    formula = generate_random_3cnf(n)
    val_width = boolean_tensor_product_width(formula)
    min_rank = min_rank_tqft(formula)
    
    if val_width == 0:
        return {
            "metric_name": "log_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "val_width=0"
        }
    
    log_ratio = math.log(min_rank) / math.log(val_width)
    conjecture_holds = log_ratio >= 1 and log_ratio <= 2
    
    return {
        "metric_name": "log_ratio",
        "metric_value": log_ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        seeds = [2**i + 3 for i in range(5, 8)]  # Default list of 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        result_type = "FALSIFIED"
    
    print(f"RESULT: {result_type} mean={mean_value} std=0 support_fraction={support_fraction}")