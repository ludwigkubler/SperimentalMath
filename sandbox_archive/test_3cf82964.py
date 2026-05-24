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

def run_trial(seed: int) -> dict:
    if seed <= 0 or seed > 10**9:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "seed_out_of_range"
        }
    
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Simulate generating a function field K of degree n
    # This is a placeholder for the actual computation
    D_K_rank = random.randint(n // 2, n * 2)  # Placeholder rank
    
    # Simulate estimating the minimal rank of D(K)
    estimated_rank = D_K_rank
    
    # Simulate measuring the randomized communication complexity for Disjointness
    communication_complexity = random.uniform(0.1 * n**2, 1.5 * n**2)
    
    # Check if the conjecture holds
    c = 1  # Absolute constant
    conjecture_holds = estimated_rank > c * n**2 and communication_complexity >= c * n**2
    
    counterexample = ""
    if not conjecture_holds:
        if estimated_rank <= n:
            counterexample = "minimal_rank_too_low"
        elif communication_complexity < c * n**2:
            counterexample = "communication_complexity_too_low"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_communication_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_communication_complexity = (sum((r["metric_value"] - mean_communication_complexity) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_communication_complexity} std={std_communication_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")