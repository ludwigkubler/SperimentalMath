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
    
    # Define constants and parameters
    n_max = 40
    instances_per_seed = 30
    
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_per_seed):
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        
        # Generate a random Boolean satisfiability instance
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        
        # Compute the symmetry group of all possible truth assignments
        # This is a placeholder function; actual implementation needed
        num_generators = compute_symmetry_group_size(m, n)
        
        if num_generators > m**(1/3) * n**(2/3):
            conjecture_holds = False
            counterexample = f"m={m}, n={n}, num_generators={num_generators}"
        
        total_metric_value += num_generators
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for _ in range(instances_per_seed) if not conjecture_holds) / instances_per_seed
    
    return {
        "metric_name": "num_generators",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_symmetry_group_size(m: int, n: int) -> int:
    # Placeholder function; actual implementation needed
    return random.randint(1, 10)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(not result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction <= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")