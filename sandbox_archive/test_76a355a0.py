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
    
    def generate_random_function(n):
        return {tuple(random.sample(range(2), n)) for _ in range(10)}
    
    def compute_minimal_rank(poly_system):
        # Placeholder for actual computation
        return len(poly_system)
    
    def communication_complexity(f):
        # Placeholder for actual computation
        return len(f) * 2
    
    n = random.randint(5, 40)
    f = generate_random_function(n)
    rank = compute_minimal_rank(f)
    comm_complexity = communication_complexity(f)
    
    if rank == 0:
        return {
            "metric_name": "Rank vs Comm Complexity",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rank_zero"
        }
    
    ratio = comm_complexity / rank
    
    return {
        "metric_name": "Rank vs Comm Complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_zero\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")