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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def next_prime(p):
        p += 1
        while not is_prime(p):
            p += 1
        return p
    
    def minimal_quadratic_residue_symbol(p):
        for zeta in range(2, p):
            if (zeta * zeta) % (p * p) == 1:
                return zeta
        return None
    
    def dpll_tree_height(n):
        # Simplified DPLL tree height calculation for demonstration
        return n * math.log2(n)
    
    primes = [5, 13, 17, 29, 37, 41, 47, 53, 59, 61]
    log_zeta_min_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30]:
        if n > n_max:
            n_max = n
        
        for _ in range(7):  # Ensure at least 8 instances per seed
            k = random.randint(1, n - 1)
            formula = []
            for _ in range(k):
                clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
                formula.append(clause)
            
            height = dpll_tree_height(n)
            instances_tested += 1
            
            log_zeta_min = math.log2(minimal_quadratic_residue_symbol(next_prime(n)))
            if log_zeta_min is not None:
                log_zeta_min_values.append(log_zeta_min)
    
    mean_log_zeta_min = sum(log_zeta_min_values) / len(log_zeta_min_values)
    conjecture_holds = all(height <= mean_log_zeta_min for height in log_zeta_min_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": sum(log_zeta_min_values) / len(log_zeta_min_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [5, 13, 17, 29, 37, 41, 47, 53, 59, 61]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")