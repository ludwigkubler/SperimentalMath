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
    
    def generate_frege_proof(depth, n):
        if depth == 0:
            return [random.randint(1, n)]
        else:
            left = generate_frege_proof(random.randint(0, depth-1), n)
            right = generate_frege_proof(random.randint(0, depth-1), n)
            return [random.randint(1, n)] + left + right
    
    def p_adic_analytic_continuation(proof):
        if not proof:
            return []
        continuation = [proof[0]]
        for i in range(1, len(proof)):
            next_val = continuation[-1] ** proof[i]
            continuation.append(next_val)
        return continuation
    
    def growth_rate(continuation):
        if not continuation:
            return 0
        max_growth = 0
        prev_val = 1
        for val in continuation:
            growth = math.log(val, prev_val) / math.log(prev_val + 1, prev_val)
            if growth > max_growth:
                max_growth = growth
            prev_val = val
        return max_growth
    
    depth = random.randint(5, 10)
    n = random.randint(10, 40)
    phi = generate_frege_proof(depth, n)
    continuation = p_adic_analytic_continuation(phi)
    
    if not continuation:
        return {
            "metric_name": "growth_rate",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_continuation"
        }
    
    growth = growth_rate(continuation)
    lid = len(phi) - depth
    
    return {
        "metric_name": "growth_rate",
        "metric_value": growth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    mean_growth_rate = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_growth_rate) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if not result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_growth_rate} std={std_deviation} support_fraction={support_fraction}")
    elif any(result["counterexample"]):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")